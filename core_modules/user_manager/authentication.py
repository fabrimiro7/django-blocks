import jwt, datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from .models import User
import secrets


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')         
            id = decode_access_token(token)
            user = User.objects.get(pk=id)

            return (user, None)

        raise exceptions.AuthenticationFailed('unauthenticated1')


def create_access_token(id, permission, user_type):
    return jwt.encode({
        'user_id': id,
        'permission': permission,
        'user_type': user_type,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
        'iat': datetime.datetime.utcnow()
    }, 'access_secret', algorithm='HS256')


def decode_access_token(token):
    try:
        payload = jwt.decode(token, 'access_secret', algorithms='HS256')
        return payload['user_id']
    except Exception:
        raise exceptions.AuthenticationFailed('unauthenticated2')


def create_refresh_token(id):
    refresh_token = jwt.encode({
        'user_id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5),
        'iat': datetime.datetime.utcnow()
    }, 'refresh_secret', algorithm='HS256')
    return refresh_token


def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, 'refresh_secret', algorithms=['HS256'])

        return payload['user_id']
    except Exception:
        raise exceptions.AuthenticationFailed('unauthenticated3')
