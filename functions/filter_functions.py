from functions.pubsub_functions import *

maxPullAttempts = 10
messagesToPull = 10

def filter_messages_by_source_subscription(subscriptionId, numberOfMessages, filter):
    try:
        sourceSubscriptionAttributeName = 'CloudPubSubDeadLetterSourceSubscription'
        filteredMessages = []

        print('starting inspection of messages')

        pullAttempt = 1
        while pullAttempt < maxPullAttempts:
            for msg in get_messages(subscriptionId, numberOfMessages):
                if sourceSubscriptionAttributeName not in msg.message.attributes:
                    print('No atrribute found for source subscription')
                    continue
                if filter.lower() in msg.message.attributes[sourceSubscriptionAttributeName].lower():
                    print('Matched atrribute')
                    filteredMessages.append(msg)
                    #publish
                    msg.message.ack()

                if len(filteredMessages) == numberOfMessages:
                    break

            pullAttempt += 1
                
        return filteredMessages

    except Exception as ex:
        print('An exception has occured trying filter messages using the filter ' + filter + ' - ' + str(ex))