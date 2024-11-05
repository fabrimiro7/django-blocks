from django.shortcuts import render
from requests import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status, generics
from edplatform.specific import REMOTE_API
from core_modules.testing.models import SingleTestElement
from core_modules.user_manager.authentication import create_access_token, JWTAuthentication, create_refresh_token, decode_refresh_token

from .serializers import SingleTestElementSerializer        

class SingleTestElementListCreateView(generics.ListCreateAPIView):
    queryset = SingleTestElement.objects.all()
    serializer_class = SingleTestElementSerializer
    if REMOTE_API == True:
        authentication_classes = [JWTAuthentication]


