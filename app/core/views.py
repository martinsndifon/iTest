"""
Core views for app
"""
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers


class HealthCheckSerializer(serializers.Serializer):
    healthy = serializers.BooleanField()


@extend_schema(tags=["health-check"], responses={200: HealthCheckSerializer})
@api_view(["GET"])
def health_check(request):
    """Returns successful response."""
    return Response({"healthy": True})
