"""Authentication middleware for client updates. """
from django.conf import settings

class APIKeyAuthenticator(object):
    def process_request(self, request):
        bearer_token = request.META.get("HTTP_AUTHORIZATION", None)
        token = None
        if bearer_token:
            token = bearer_token.split(' ')[1]
        # Check authentication token
        authenticated = False
        if token and token == settings.API_KEY_UPDATE:
            authenticated = True
        setattr(request,'authenticated', authenticated)
        return None
