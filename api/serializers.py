from rest_framework import serializers
from .models import links

class LinkSerializers(serializers.ModelSerializer):
    class Meta:
        model = links
        fields = (
            'lid', 'link', 'trough', 'api_key', 'created_on'
        )