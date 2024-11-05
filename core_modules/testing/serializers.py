from .models import SingleTestElement
from rest_framework import serializers



class SingleTestElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleTestElement
        fields = ['title']