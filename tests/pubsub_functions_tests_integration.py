
from functions.pubsub_functions import *
import os

def test_topic_exists_returns_true_when_topic_exists_in_project():
    #arrange
    os.environ['PROJECT_ID'] = 'ons-blaise-dev-jam39'
    topicId = 'new-case-topic'

    #act
    result = pubsub_functions.topic_exists(topicId)

    #assert
    assert result == True

def test_topic_exists_returns_false_when_topic_does_not_exist_in_project():
    #arrange
    os.environ['PROJECT_ID'] = 'ons-blaise-dev-jam39'
    topicId = 'topic-does-not-exist'

    #act
    result = pubsub_functions.topic_exists(topicId)

    # Call tested function
    assert result == False

def test_subscription_exists_returns_true_when_subscription_exists_in_project():
    #arrange
    os.environ['PROJECT_ID'] = 'ons-blaise-dev-jam39'
    subscriptionId = 'blaise-deadletter-subscription'

    #act
    result = pubsub_functions.subscription_exists(subscriptionId)

    #assert
    assert result == True

def test_subscription_exists_returns_false_when_subscription_does_not_exist_in_project():
    #arrange
    os.environ['PROJECT_ID'] = 'ons-blaise-dev-jam39'
    subscriptionId = 'subscription-does-not-exist'

    #act
    result = pubsub_functions.subscription_exists(subscriptionId)

    #assert
    assert result == False