import time
import threading
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


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.number_of_messages = 0
        self.timer = self.timer_function()

    def __call__(self, request):
        client_ip = self.get_client_ip(request)

        if self.number_of_messages >= 5 and not self.timer.is_alive():
            return HttpResponseForbidden("You cannot send more than 5 messages per minute")

        self.number_of_messages += 1
        response = self.get_response(request)

        return response
    
    def timer_function(self):
        print("timer_start")

        def timer_complete():
            pass
            # timer.start()

        timer = threading.Timer(60.0, timer_complete)
        timer.start()

        return timer

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip
