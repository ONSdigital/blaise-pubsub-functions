from unittest.mock import Mock

from functions.main import *
import os

def test_function_runs_when_data_is_provided():
    #arrange
    data = { "DeadletterSubscription": "blaise-deadletter-subscription",
             "PublishToTopic": "new-case-topic",
             "SourceSubscriptionFilter": "new-case-subscription" }
    request = Mock(get_json=Mock(return_value=data))
    os.environ['PROJECT_ID'] = 'ons-blaise-dev-jam39'

    #act
    result = Replay_Deadletter_Messages(request)

    #assert
    assert result == 'Topic new-case-topic found!'
