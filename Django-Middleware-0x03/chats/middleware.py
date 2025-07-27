import time
from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        with open('requests.log', "+a") as f:
            now = datetime.now()
            user = request.user
            path = request.path

            f.write(f'{now} - User: {user} - Path: {path}\n')
            # print(f'{now} - User: {user} - Path: {path}\n')

        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = time.localtime()
        current_hour = current_time.tm_hour
        formatted_time = time.strftime("%H:%M:%S", current_time)

        if not 18 <= current_hour < 21:
            print(f"Current Time: {formatted_time}")
            return HttpResponseForbidden("You are not allowed to send messages outside 6pm and 9pm")

        response = self.get_response(request)

        return response
