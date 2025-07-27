from datetime import datetime


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
            print(f'{now} - User: {user} - Path: {path}\n')

        return response
