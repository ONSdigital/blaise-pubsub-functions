import sys
import os

from flask import escape
from google.cloud import pubsub_v1
from pubsub_helper import PubSubHelper

def Replay_Deadletter_Messages(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    
    request_json = request.get_json(silent=True)

    if request_json and 'DeadletterSubscription' in request_json:
        deadletterSubscription = request_json['DeadletterSubscription']
        print('Dead-letter Subscription is set to - ' + deadletterSubscription)
    else:
        return 'You must specify the deadletter subscription to pull from'    

    if request_json and 'PublishToTopic' in request_json:
        publishToTopic = request_json['PublishToTopic']
        print('Publish To Topic is set to - ' + publishToTopic)
    else:
        return 'You must specify the topic you wish to post the message to'

    if request_json and 'SourceSubscriptionFilter' in request_json:
        sourceSubscriptionFilter = request_json['SourceSubscriptionFilter']
        print('Source Subscription Filter is set to - ' + sourceSubscriptionFilter)
    else:
        return 'You must specify a filter you wish to restrict which messages are retrieved from the dead-letter subscription'


    client = pubsub_v1.PublisherClient()
    print('instantiated client')
    
    projectId = os.environ.get('PROJECT_ID')
    project = client.project_path(projectId)
    print('The google project is set to - ' + projectId)

 
    for topic in client.list_topics(project):
        dir(topic)
        if topic.name.lower().endswith(publishToTopic.lower()):
          return 'Topic {} found!'.format(escape(publishToTopic))

    return 'Topic {} not found in project!'.format(escape(publishToTopic))


