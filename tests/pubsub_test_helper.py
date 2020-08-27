from google.cloud import pubsub_v1
import os


def publish_message(topicId, message, sourceSubscription):
    client = pubsub_v1.PublisherClient()
    projectId = os.environ.get('PROJECT_ID')
    topicPath = client.topic_path(projectId, topicId)

    data = message.encode("utf-8")
    client.publish(topicPath, data=data, CloudPubSubDeadLetterSourceSubscription=sourceSubscription)
    print("published message ", data)
            