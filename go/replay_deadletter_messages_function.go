package main

import (
	"context"
	"fmt"
	"log"
	"sync"
	"time"

	"cloud.google.com/go/pubsub"
	"google.golang.org/api/option"
)

var (
	topic              *pubsub.Topic
	googleCloudProject = "ons-blaise-dev-jam39"
	topicId            = "blaise-deadletter-test-topic"
	subscriptionId     = "blaise-deadletter-test-subscription"
	sourceSubscription = "subscription-tel"
)

const maxMessages = 10
const subscriptionSourceAttributeName = "CloudPubSubDeadLetterSourceSubscription"
const credentialsPath = "/users/jamiekerr/Downloads/ons-blaise-dev-jam39-6de66e990a49.json"
const timeoutInSeconds = 30 * time.Second

func main() {
	log.Println("Started")

	err := processMessages(googleCloudProject, subscriptionId, maxMessages)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("Finished")
}

func processMessages(projectId, subscriptionId string, limitMessages int) error {
	ctx := context.Background()

	client, err := pubsub.NewClient(ctx, projectId, option.WithCredentialsFile(credentialsPath))
	if err != nil {
		log.Fatal(err)
		return fmt.Errorf("pubsub.NewClient: %v", err)
	}

	//consume messages
	var mu sync.Mutex
	processedMessages := 0
	sub := client.Subscription(subscriptionId)

	cctx, cancel := context.WithTimeout(ctx, timeoutInSeconds)

	err = sub.Receive(cctx, func(ctx context.Context, msg *pubsub.Message) {
		mu.Lock()
		defer mu.Unlock()

		if messageMatchesAttributeFilter(msg, subscriptionSourceAttributeName, sourceSubscription) {
			log.Println("Got message with id" + msg.ID + " data " + string(msg.Data))
			processedMessages++
			//TODO: publish message to topic to replay
			msg.Ack()
		} else {
			log.Println("ignored message with id" + msg.ID + " data " + string(msg.Data))
			msg.Nack()
		}

		if processedMessages == limitMessages {
			cancel()
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
