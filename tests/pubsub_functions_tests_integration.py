
from functions.pubsub_functions import *
import os

def test_topic_exists_returns_true_when_topic_exists_in_project():
    #arrange
    os.environ['PROJECT_ID'] = 'ons-blaise-dev-jam39'
    topicId = 'new-case-topic'

    #act
    result = topic_exists(topicId)

    #assert
    assert result == True

def test_topic_exists_returns_false_when_topic_does_not_exist_in_project():
    #arrange
    os.environ['PROJECT_ID'] = 'ons-blaise-dev-jam39'
    topicId = 'topic-does-not-exist'

    #act
    result = topic_exists(topicId)

    # Call tested function
    assert result == False

def test_subscription_exists_returns_true_when_subscription_exists_in_project():
    #arrange
    os.environ['PROJECT_ID'] = 'ons-blaise-dev-jam39'
    subscriptionId = 'blaise-deadletter-subscription'

    #act
    result = subscription_exists(subscriptionId)

    #assert
    assert result == True

def test_subscription_exists_returns_false_when_subscription_does_not_exist_in_project():
    #arrange
    os.environ['PROJECT_ID'] = 'ons-blaise-dev-jam39'
    subscriptionId = 'subscription-does-not-exist'

    #act
    result = subscription_exists(subscriptionId)

    #assert
    assert result == False

def test_get_messages_returns_messages_if_they_exist_in_subscription():
    #arrange
    os.environ['PROJECT_ID'] = 'ons-blaise-dev-jam39'
    subscriptionId = 'blaise-deadletter-test-subscription'

    #act
    result = get_messages(subscriptionId, 1)
    print(result)
    #assert
    assert result is not None