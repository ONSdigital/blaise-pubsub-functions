import sys
import os
from functions.pubsub_functions import *
from functions.input_functions import *

from flask import escape

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

    deadletterSubscription = get_argument_from_request(request_json, 'DeadletterSubscription')
    if deadletterSubscription is None or subscription_exists(deadletterSubscription) == False:
        return 'You must specify a valid subscription to pull from deadletter messages from'  

    publishToTopic = get_argument_from_request(request_json, 'PublishToTopic')
    if publishToTopic is None or topic_exists(publishToTopic) == False:
        return 'You must specify a valid topic that you wish to post the deadletter message to'

    sourceSubscriptionFilter = get_argument_from_request(request_json, 'SourceSubscriptionFilter')
    if sourceSubscriptionFilter is None:
        return 'You must specify a filter you wish to restrict which messages are retrieved from the dead-letter subscription'


    return 'Topic {} found!'.format(escape(publishToTopic))


