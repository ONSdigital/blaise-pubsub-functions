
import pubsub_functions
import os

def test_topic_exists_returns_true_when_topic_exists_in_project():
    os.environ['PROJECT_ID'] = 'ons-blaise-dev-jam39'
    topicId = 'new-case-topic'

    # Call tested function
   
    assert pubsub_functions.topic_exists(topicId) == True

def test_topic_exists_returns_false_when_topic_does_not_exist_in_project():
    os.environ['PROJECT_ID'] = 'ons-blaise-dev-jam39'
    topicId = 'topic-does-not-exist'

    # Call tested function
   
    assert pubsub_functions.topic_exists(topicId) == False