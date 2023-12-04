import time

from django.http.request import HttpRequest


class ResponseTimeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):

        start = time.time()

        response = self.get_response(request)

        end = time.time()

        self._log(f"{end-start} {request.method} {request.path}")

        return response
    
    def _log(self, msg):

        with open('logs/response_time.log', 'a') as log:
            log.write(f"\n{msg}")