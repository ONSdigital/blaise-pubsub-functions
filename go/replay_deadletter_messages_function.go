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

	subscriptionFilter = "subscription-tel"
	credentialsPath    = "/users/jamiekerr/Downloads/ons-blaise-dev-jam39-6de66e990a49.json"
	messages           []string
)

const maxMessages = 10
const subscriptionSourceFilterName = "CloudPubSubDeadLetterSourceSubscription"

func main() {
	ctx := context.Background()
	client, err := pubsub.NewClient(ctx, googleCloudProject, option.WithCredentialsFile(credentialsPath))
	if err != nil {
		log.Fatal(err)
	}

	topic = client.Topic(topicId)

	exists, err := topic.Exists(ctx)
	if err != nil {
		log.Fatal(err)
	}

	if exists {
		log.Println("Topic exists")
	} else {
		log.Println("Topic does not exist")
	}

	err = pullMessages(googleCloudProject, subscriptionId, maxMessages)
	if err != nil {
		log.Fatal(err)
	}
}

func pullMessages(projectId, subscriptionId string, limitMessages int) error {
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
	cctx, cancel := context.WithTimeout(ctx, 120*time.Second)

	err = sub.Receive(cctx, func(ctx context.Context, msg *pubsub.Message) {
		mu.Lock()
		defer mu.Unlock()

		if processMessage(msg) {
			log.Println("Got message with id" + msg.ID + " data " + string(msg.Data))
			processedMessages++
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

	log.Println("Complete")
	return nil
}

func processMessage(msg *pubsub.Message) bool {
	if val, ok := msg.Attributes[subscriptionSourceFilterName]; ok {
		if val == subscriptionFilter {
			return true
		}
	}

	return false
}
