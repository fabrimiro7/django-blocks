import jwt
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None

        prefix, token = auth_data.decode("utf-8").split(" ")

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY)
            user = User.objects.get(username=payload["username"])
            return (user, token)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(_("Invalid Token, login again"))
