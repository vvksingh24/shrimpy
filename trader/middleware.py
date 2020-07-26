import json
import time

from rest_framework.response import Response

class ResponseTimeMiddleware(object):
    '''
    middleware for calculating response time
    '''

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called
        start_time = time.time()
        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called.
        duration = time.time() - start_time

        return response
