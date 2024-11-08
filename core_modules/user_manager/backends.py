import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from .models import User


class JWTAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None

        prefix, token = auth_data.decode('utf-8').split(' ')

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY)
            user = User.objects.get(username=payload['username'])
            return (user, token)
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed('Token non valido, login')

        return super().authenticate(request)

