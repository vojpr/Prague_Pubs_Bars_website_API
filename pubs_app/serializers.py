from rest_framework import serializers
from .models import PubsBars


class PubsBarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PubsBars
        fields = "__all__"