import os

from google.cloud import pubsub_v1

def topic_exists(topicId):
    try:
        client = pubsub_v1.PublisherClient()
        projectId = os.environ.get('PROJECT_ID')
        project = client.project_path(projectId)
                
        for topic in client.list_topics(project):
            if topic.name.lower().endswith(topicId.lower()):
                return True

        return False

    except Exception as ex:
        print('An exception has occured - ' + str(ex))
       