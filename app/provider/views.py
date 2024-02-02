"""
views for the provider API.
"""
from drf_spectacular.utils import extend_schema

from rest_framework import viewsets

from core.models import Provider
from provider import serializers


@extend_schema(tags=["provider"])
class ProviderViewSet(viewsets.ModelViewSet):
    """View for managing provider API."""

    serializer_class = serializers.ProviderSerializer
    queryset = Provider.objects.all().order_by("-provider_no")
