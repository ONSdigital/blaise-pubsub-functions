import sys
import os
from functions.pubsub_functions import *
from functions.input_functions import *

from flask import escape

def Replay_Deadletter_Messages(request):
    """HTTP Cloud Function.
    Args:

    Returns:

    """
    
    request_json = request.get_json(silent=True)

    deadletterSubscriptionId = get_argument_from_request(request_json, 'DeadletterSubscription')
    if deadletterSubscriptionId is None or subscription_exists(deadletterSubscriptionId) == False:
        return 'You must specify a valid subscription to pull from deadletter messages from'  

    publishToTopicId = get_argument_from_request(request_json, 'PublishToTopic')
    if publishToTopicId is None or topic_exists(publishToTopicId) == False:
        return 'You must specify a valid topic that you wish to post the deadletter message to'

    subscriptionFilter = get_argument_from_request(request_json, 'SourceSubscriptionFilter')
    if subscriptionFilter is None:
        return 'You must specify a filter you wish to restrict which messages are retrieved from the dead-letter subscription'
    
    for msg in get_filtered_messages(subscriptionFilter, deadletterSubscriptionId, 1):
        print(msg)

    return 'Topic {} found!'.format(escape(publishToTopicId))


