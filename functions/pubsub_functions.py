import os

from google.cloud import pubsub_v1

def create_topic(topicId):
    try:
        client = pubsub_v1.PublisherClient()
        topicPath = get_topic_path(topicId)

        if not topic_exists(topicId):
            client.create_topic(topicPath)
            print('Created topic', topicId)

    except Exception as ex:
        print('An exception has occured trying to create the topic ' + topicId + ' - ' + str(ex))

def delete_topic(topicId):
    try:
        client = pubsub_v1.PublisherClient()
        topicPath = get_topic_path(topicId)

        if topic_exists(topicId):
            client.delete_topic(topicPath)
            print('Deleted topic', topicId)

    except Exception as ex:
        print('An exception has occured trying to delete the topic ' + topicId + ' - ' + str(ex))

def create_subscription(topicId, subscriptionId):
    try:
        client = pubsub_v1.SubscriberClient()
        topicPath = get_topic_path(topicId)
        subscriptionPath = get_subscription_path(subscriptionId)

        if not subscription_exists(subscriptionId):
            client.create_subscription(subscriptionPath, topicPath)
            print('Created subscription', subscriptionId)

    except Exception as ex:
        print('An exception has occured trying to create the subscription ' + subscriptionId + '- ' + str(ex))

def delete_subscription(subscriptionId):
    try:
        client = pubsub_v1.SubscriberClient()
        subscriptionPath = get_subscription_path(subscriptionId)

        if subscription_exists(subscriptionId):
            client.delete_subscription(subscriptionPath)
            print('Deleted subscription', subscriptionId)

    except Exception as ex:
        print('An exception has occured trying to delete the subscription ' + subscriptionId + '- ' + str(ex))

def topic_exists(topicId):
    try:
        client = pubsub_v1.PublisherClient()
        projectPath = get_project_path()
                
        for topic in client.list_topics(projectPath):
            if topic.name.lower().endswith(topicId.lower()):
                return True

        return False

    except Exception as ex:
        print('An exception has occured trying to determine if the topic ' + topicId + ' exists- ' + str(ex))

def subscription_exists(subscriptionId):
    try:
        client = pubsub_v1.SubscriberClient()
        projectPath = get_project_path()
                
        for subscription in client.list_subscriptions(projectPath):
            if subscription.name.lower().endswith(subscriptionId.lower()):
                return True

        return False

    except Exception as ex:
        print('An exception has occured trying to determine if the subscription ' + subscriptionId + ' exists- ' + str(ex))

def get_messages(subscriptionId, numberOfMessages):
    try:
        client = pubsub_v1.SubscriberClient()
        subscriptionPath = get_subscription_path(subscriptionId)

        response = client.pull(subscriptionPath, numberOfMessages)
        return response.received_messages

    except Exception as ex:
        print('An exception has occured trying to pull messages from the subscription ' + subscriptionId + ' - ' + str(ex))

def get_project_path():
    try:
        client = pubsub_v1.PublisherClient()
        projectId = get_project_id()
        return client.project_path(projectId)

    except Exception as ex:
        print('An exception has occured trying to get the project path- ' + str(ex))

def get_topic_path(topicId):
    try:
        client = pubsub_v1.PublisherClient()
        projectId = get_project_id()

        return client.topic_path(projectId, topicId)

    except Exception as ex:
        print('An exception has occured trying to get the topic path - ' + str(ex))

def get_subscription_path(subscriptionId):
    try:
        client = pubsub_v1.SubscriberClient()
        projectId = get_project_id()

        return client.subscription_path(projectId, subscriptionId)

    except Exception as ex:
        print('An exception has occured trying to get the subscription path - ' + str(ex))

def get_project_id():
    try:
        return os.environ.get('PROJECT_ID')

    except Exception as ex:
        print('An exception has occured trying to get the GCP projectId environment varioable - ' + str(ex))