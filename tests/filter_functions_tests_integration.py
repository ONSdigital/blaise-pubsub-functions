
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

    i = 1
    while i < 200:
        publish_message(topicId, 'Test body ' + str(i), 'subscription-val')
        i += 1

    publish_message(topicId, 'Hooray 1', filter)

    
    #act
    result = filter_messages_by_source_subscription(subscriptionId, 2, filter)

    delete_subscription(subscriptionId)
    delete_topic(topicId)

    #assert
    assert len(result) == 1
    
