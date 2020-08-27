
from functions.input_functions import *

def test_get_argument_from_request_returns_argument_if_the_argument_exists():
    #arrange
    request = { "PublishToTopic": "new-case-topic", 
             "SourceSubscriptionFilter": "new-case-subscription" }
    
    #act
    result = get_argument_from_request(request, 'PublishToTopic')

    #assert
    assert result == 'new-case-topic'

def test_get_argument_from_request_returns_none_if_the_argument_does_not_exist():
    #arrange
    request = { "PublishToTopic": "new-case-topic", 
             "SourceSubscriptionFilter": "new-case-subscription" }
    
    #act
    result = get_argument_from_request(request, 'ArgumentDoesNotexist')

    #assert
    assert result is None