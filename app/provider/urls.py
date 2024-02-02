"""
URL mappings for the provider app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from provider import views

router = DefaultRouter()
router.register("", views.ProviderViewSet)

app_name = "provider"

urlpatterns = [
    path("", include(router.urls)),
]
