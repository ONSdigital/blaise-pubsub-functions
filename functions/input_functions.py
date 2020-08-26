
def get_argument_from_request(request, argument):
    try:
        if request and argument in request:
            return request[argument]
        else:
            return None

    except Exception as ex:
        print('An exception has occured trying to retrieve the argument ' + argument + ' - ' + str(ex))
