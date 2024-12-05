from rest_framework import generics

from core_modules.user_manager.authentication import JWTAuthentication  # noqa
from edplatform.specific import REMOTE_API
from .models import SingleTestElement
from .serializers import SingleTestElementSerializer


class SingleTestElementListCreateView(generics.ListCreateAPIView):
    queryset = SingleTestElement.objects.all()
    serializer_class = SingleTestElementSerializer
    if REMOTE_API is True:
        authentication_classes = [JWTAuthentication]
