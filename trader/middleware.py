import json
import time

from rest_framework.response import Response


class ResponseTimeMiddleware(object):
    '''
    middleware for calculating response time
    '''

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # get time before the view (and later middleware) are called
        start_time = time.time()
        response = self.get_response(request)

        # Calculate time after the view is called.
        duration = time.time() - start_time
        # uncomment this code to get response time in response body
        # if isinstance(response, Response):
        #     response.data['time'] = f'{duration * 1000}ms'
        #     response._is_rendered = False
        #     response.render()

        # add response time to header
        response["X-total-time-ms"] = duration * 1000
        return response
