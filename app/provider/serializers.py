"""
Serializers for provider APIs.
"""
from rest_framework import serializers
from core.models import Provider


class ProviderSerializer(serializers.ModelSerializer):
    """Serializer for provider objects."""

    class Meta:
        model = Provider
        fields = [
            "provider_no",
            "provider_name",
        ]
        read_only_fields = ["provider_no"]
