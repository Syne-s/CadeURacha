from django.shortcuts import redirect
import re
from django.http import JsonResponse

class UsernameValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Check username validity
            pattern = re.compile(r'^[a-zA-Z](?!.*__)[a-zA-Z0-9]*(_[a-zA-Z0-9]+)*$')
            username = request.user.username
            
            if not pattern.match(username) or len(username) < 4 or len(username) > 20:
                request.invalid_username = True
        
        response = self.get_response(request)
        return response