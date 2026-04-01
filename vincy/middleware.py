# vincy/middleware.py
from django.http import JsonResponse
from django.urls import resolve
from django.shortcuts import redirect

class ApiAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path starts with /admin/api/
        if request.path.startswith('/admin/api/'):
            # Don't redirect API requests to login
            # Just check if user is admin via session
            if request.session.get('type') != 'admin':
                return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)
        
        response = self.get_response(request)
        return response


class DisableAuthMiddleware:
    """Middleware to disable authentication for API endpoints"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip authentication for API endpoints
        if request.path.startswith('/admin/api/'):
            # Store original LOGIN_URL temporarily
            from django.conf import settings
            original_login_url = settings.LOGIN_URL
            
            # Temporarily disable LOGIN_URL for this request
            settings.LOGIN_URL = None
            
            response = self.get_response(request)
            
            # Restore original LOGIN_URL
            settings.LOGIN_URL = original_login_url
            
            return response
        
        response = self.get_response(request)
        return response