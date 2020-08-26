import os

from google.cloud import pubsub_v1

def topic_exists(topicId):
    try:
        client = pubsub_v1.PublisherClient()
        project = get_project()
                
        for topic in client.list_topics(project):
            if topic.name.lower().endswith(topicId.lower()):
                return True

        return False

    except Exception as ex:
        print('An exception has occured trying to determine if the topic ' + topicId + ' exists- ' + str(ex))

def subscription_exists(subscriptionId):
    try:
        client = pubsub_v1.SubscriberClient()
        project = get_project()
                
        for subscription in client.list_subscriptions(project):
            if subscription.name.lower().endswith(subscriptionId.lower()):
                return True

        return False

    except Exception as ex:
        print('An exception has occured trying to determine if the subscription ' + subscriptionId + ' exists- ' + str(ex))

def get_project():
    try:
        client = pubsub_v1.PublisherClient()
        projectId = os.environ.get('PROJECT_ID')
        return client.project_path(projectId)

    except Exception as ex:
        print('An exception has occured trying to get the GCP project - ' + str(ex))