from unittest.mock import Mock

import main
import os

def test_function_runs_when_data_is_provided():
    data = { "DeadletterSubscription": "blaise-deadletter-subscription",
             "PublishToTopic": "new-case-topic",
             "SourceSubscriptionFilter": "new-case-subscription" }
    req = Mock(get_json=Mock(return_value=data))
    os.environ['PROJECT_ID'] = 'ons-blaise-dev-jam39'

    # Call tested function
    assert main.Replay_Deadletter_Messages(req) == 'Topic new-case-topic found!'
