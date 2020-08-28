package main

import (
	"context"
	"fmt"
	"log"
	"sync"
	"time"

	"cloud.google.com/go/pubsub"
	"google.golang.org/api/option"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

var (
	topic                      *pubsub.Topic
	googleCloudProject         = "ons-blaise-dev-jam39"
	topicId                    = "blaise-deadletter-test-topic"
	subscriptionId             = "blaise-deadletter-test-subscription"
	sourceSubscription         = "subscription-tel"
	lastTimeOfRecordedActivity = time.Now()
)

const subscriptionSourceAttributeName = "CloudPubSubDeadLetterSourceSubscription"
const credentialsPath = "/users/jamiekerr/Downloads/ons-blaise-dev-jam39-6de66e990a49.json"
const timeout = 30 * time.Second

func main() {
	fmt.Println("Started")

	err := processMessagesInSubscriptionSync(subscriptionId)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Finished")
}

func cancelContextDueToInactivity(cancel context.CancelFunc) {

	for {
		time.Sleep(10 * time.Second)

		fmt.Println("Last activity = " + lastTimeOfRecordedActivity.String())
		diff := time.Now().Sub(lastTimeOfRecordedActivity)
		if diff.Seconds() > 30 {
			fmt.Println("Cancelling due to inactivity")
			cancel()
		}
	}
}

var processedMessages = 0

func testBgTask(cancel context.CancelFunc) {

	for {
		time.Sleep(5 * time.Second)

		fmt.Println("Processed messages " + fmt.Sprint(processedMessages))
	}
}

func processMessagesInSubscription(subscriptionId string) error {
	ctx := context.Background()

	client, err := pubsub.NewClient(ctx, googleCloudProject, option.WithCredentialsFile(credentialsPath))
	if err != nil {
		log.Fatal(err)
		return fmt.Errorf("pubsub.NewClient: %v", err)
	}

	var mu sync.Mutex

	sub := client.Subscription(subscriptionId)

	cctx, cancel := context.WithTimeout(ctx, timeout)

	//go cancelContextDueToInactivity(cancel)

	err = sub.Receive(cctx, func(ctx context.Context, msg *pubsub.Message) {
		processedMessages++
		mu.Lock()
		defer mu.Unlock()

		lastTimeOfRecordedActivity = time.Now()
		if messageMatchesAttributeFilter(msg, subscriptionSourceAttributeName, sourceSubscription) {
			fmt.Println("Got message with id" + msg.ID + " data " + string(msg.Data) + " at - " + time.Now().String())

			//TODO: publish message to topic to replay
			msg.Ack()
		} else {
			fmt.Println("ignored message with id" + msg.ID + " data " + string(msg.Data) + " at - " + time.Now().String())
			msg.Ack()
		}

		select {
		case <-ctx.Done():
			cancel()
		}
	})
	if err != nil {
		log.Fatal(err)
		return fmt.Errorf("Receive: %v", err)
	}

	fmt.Println("processed " + fmt.Sprint(processedMessages) + " messages")
	return nil
}

func messageMatchesAttributeFilter(msg *pubsub.Message, attributeName, attributeFilter string) bool {
	if val, ok := msg.Attributes[attributeName]; ok {
		if val == attributeFilter {
			return true
		}
	}

	return false
}

func processMessagesInSubscriptionSync(subID string) error {

	ctx := context.Background()
	client, err := pubsub.NewClient(ctx, googleCloudProject, option.WithCredentialsFile(credentialsPath))
	if err != nil {
		return fmt.Errorf("pubsub.NewClient: %v", err)
	}
	defer client.Close()

	sub := client.Subscription(subID)

	// Turn on synchronous mode. This makes the subscriber use the Pull RPC rather
	// than the StreamingPull RPC, which is useful for guaranteeing MaxOutstandingMessages,
	// the max number of messages the client will hold in memory at a time.
	sub.ReceiveSettings.Synchronous = true
	sub.ReceiveSettings.MaxOutstandingMessages = 5

	// Receive messages for 5 seconds.
	ctx, cancel := context.WithTimeout(ctx, 300*time.Second)
	defer cancel()

	// Create a channel to handle messages to as they come in.
	messageChannel := make(chan *pubsub.Message)
	defer close(messageChannel)

	i := 0

	lastTimeOfRecordedActivity = time.Now()
	go cancelContextDueToInactivity(cancel)

	var listIds []string
	// Handle individual messages in a goroutine.
	go func() {
		for msg := range messageChannel {
			lastTimeOfRecordedActivity = time.Now()

			if stringInSlice(msg.ID, listIds) {
				fmt.Println("duplicate message " + string(msg.Data))
				msg.Ack()
			} else {
				i++
				fmt.Println("Got message " + string(msg.Data))
			}
		}
	}()

	// Receive blocks until the passed in context is done.
	err = sub.Receive(ctx, func(ctx context.Context, msg *pubsub.Message) {
		messageChannel <- msg
	})
	if err != nil && status.Code(err) != codes.Canceled {
		return fmt.Errorf("Receive: %v", err)
	}

	fmt.Println("processed " + fmt.Sprint(i) + " messages")

	return nil
}

func stringInSlice(a string, list []string) bool {
	for _, b := range list {
		if b == a {
			return true
		}
	}
	return false
}
