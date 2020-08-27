
from functions.filter_functions import *
from tests.pubsub_test_helper import *

import os
import time

def test_filter_messages_by_source_returns_results_when_messages_matching_filter_exists():
    #arrange
    os.environ['PROJECT_ID'] = 'ons-blaise-dev-jam39'
    filter = 'subscription-tel'
    topicId = 'blaise-deadletter-test-topic'
    subscriptionId = 'blaise-deadletter-test-subscription'

    delete_subscription(subscriptionId)
    delete_topic(topicId)
    create_topic(topicId)
    create_subscription(topicId, subscriptionId)

    """publish_message(topicId, 'Test body 1', 'subscription-val')
    publish_message(topicId, 'Test body 2', filter)
    publish_message(topicId, 'Test body 3', filter)
    publish_message(topicId, 'Test body 4', 'subscription-val')
    publish_message(topicId, 'Test body 5', 'subscription-val')
    publish_message(topicId, 'Test body 6', filter)
    publish_message(topicId, 'Test body 7', filter)
    publish_message(topicId, 'Test body 8', 'subscription-val')
    publish_message(topicId, 'Test body 9', 'subscription-val')
    publish_message(topicId, 'Test body 10', 'subscription-val')
    publish_message(topicId, 'Test body 11', 'subscription-val')
    publish_message(topicId, 'Test body 12', 'subscription-val')
    publish_message(topicId, 'Test body 13', 'subscription-val')
    publish_message(topicId, 'Test body 14', 'subscription-val')
    publish_message(topicId, 'Test body 15', 'subscription-val')
    publish_message(topicId, 'Test body 16', 'subscription-val')
    publish_message(topicId, 'Test body 17', 'subscription-val')
    publish_message(topicId, 'Test body 18', 'subscription-val')
    publish_message(topicId, 'Test body 19', 'subscription-val')
    publish_message(topicId, 'Test body 20', 'subscription-val')"""

    i = 1
    while i < 200:
        publish_message(topicId, 'Test body ' + str(i), 'subscription-val')
        i += 1

    publish_message(topicId, 'Hooray 1', filter)

    
    #act
    #result = filter_messages_by_source_subscription(subscriptionId, 2, filter)

    #delete_subscription(subscriptionId)
    #delete_topic(topicId)

    #assert
    #assert len(result) == 2
    
