from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status, generics
from edplatform.specific import REMOTE_API
from core_modules.testing.models import SingleTestElement
from core_modules.user_manager.authentication import create_access_token, JWTAuthentication, create_refresh_token, \
    decode_refresh_token
from .tasks import *
from .serializers import SingleTestElementSerializer


class SingleTestElementListCreateView(generics.ListCreateAPIView):
    queryset = SingleTestElement.objects.all()
    serializer_class = SingleTestElementSerializer
    if REMOTE_API == True:
        authentication_classes = [JWTAuthentication]


class AggiungiTaskAddView(generics.ListCreateAPIView):
    queryset = SingleTestElement.objects.all()
    serializer_class = SingleTestElementSerializer

    def get(self, request, *args, **kwargs):
        # Invia il task a Celery (viene eseguito in background)
        add.delay(5, 5)  # risultato deve essere x + y
        return Response({"message": "TASK INSERITO"})


class AggiungiTaskStampaView(generics.ListCreateAPIView):
    queryset = SingleTestElement.objects.all()
    serializer_class = SingleTestElementSerializer

    def get(self, request, *args, **kwargs):
        # Invia il task a Celery (viene eseguito in background)
        stampa.delay("fabri e gio vi amo")  # risultato deve essere x + y
        # It's common to return a response, even if it's just a success message.
        return Response({"message": "TASK INSERITO"})



