from rest_framework import serializers

from .models import SingleTestElement


class SingleTestElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleTestElement
        fields = ["title"]
