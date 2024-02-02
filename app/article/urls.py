"""
URL mappings for the article app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from article import views

router = DefaultRouter()
router.register("", views.ArticleViewSet)
router.register("articles/filter", views.PriceFilterViewSet, basename="price-filter")
router.register("articles/provider", views.ProviderFilterViewSet, basename="provider-filter")

app_name = "article"

urlpatterns = [
    path("", include(router.urls)),
]
