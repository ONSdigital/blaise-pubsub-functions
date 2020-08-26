from unittest.mock import Mock

from functions.main import *

def test_deadletter_subscription_is_provided():
    #arrange
    data = { "PublishToTopic": "new-case-topic", 
             "SourceSubscriptionFilter": "new-case-subscription" }
    request = Mock(get_json=Mock(return_value=data))

    #act
    result = main.Replay_Deadletter_Messages(request)

    #assert
    assert result == 'You must specify the deadletter subscription to pull from'\
        
def test_topic_to_publish_to_is_provided():
    #arrange
    data = { "DeadletterSubscription": "blaise-deadletter-subscription",
             "SourceSubscriptionFilter": "new-case-subscription" }
    request = Mock(get_json=Mock(return_value=data))

    #act
    result = main.Replay_Deadletter_Messages(request)

    #assert
    assert result == 'You must specify the topic you wish to post the message to'\

def test_source_subscription_filter_is_provided():
    #arrange
    data = { "DeadletterSubscription": "blaise-deadletter-subscription",
             "PublishToTopic": "new-case-topic" }
    request = Mock(get_json=Mock(return_value=data))

    #act
    result = main.Replay_Deadletter_Messages(request)

    #assert
    assert result == 'You must specify a filter you wish to restrict which messages are retrieved from the dead-letter subscription'