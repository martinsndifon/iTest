"""
views for the article API.
"""
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import viewsets, mixins

from core.models import Article
from article import serializers


@extend_schema(tags=["article"])
class ArticleViewSet(viewsets.ModelViewSet):
    """View for managing article API."""

    serializer_class = serializers.ArticleSerializer
    queryset = Article.objects.all().order_by("-article_no")


@extend_schema(
    tags=["article"],
    parameters=[
        OpenApiParameter(
            "min",
            OpenApiTypes.INT,
            description="Minimum price of the article.",
        ),
        OpenApiParameter(
            "max",
            OpenApiTypes.INT,
            description="Maximum price of the article.",
        ),
    ],
)
class PriceFilterViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """View for managing price filter of article API."""

    serializer_class = serializers.ArticleSerializer
    queryset = Article.objects.all()

    def get_queryset(self):
        """Return the articles that match the filter price."""
        queryset = self.queryset
        min_price = self.request.query_params.get("min")
        max_price = self.request.query_params.get("max")

        # Convert min_price and max_price to integers if they exist
        try:
            min_price = int(min_price) if min_price else None
            max_price = int(max_price) if max_price else None
        except ValueError:
            min_price = None
            max_price = None

        # Apply price filter
        if min_price and max_price:
            queryset = queryset.filter(price__range=(min_price, max_price))
        elif min_price:
            queryset = queryset.filter(price__gte=min_price)
        elif max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset.order_by("-article_no").distinct()


@extend_schema(
    tags=["article"],
    parameters=[
        OpenApiParameter(
            "pid",
            OpenApiTypes.INT,
            description="id of the article.",
        ),
    ],
)
class ProviderFilterViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """View for managing article filter of article API."""

    serializer_class = serializers.ArticleSerializer
    queryset = Article.objects.all()

    def get_queryset(self):
        """Return the articles by a given provider."""
        queryset = self.queryset
        p_id = self.request.query_params.get("pid")

        try:
            p_id = int(p_id) if p_id else None
        except ValueError:
            p_id = None

        if p_id:
            queryset = queryset.filter(provider_no=p_id)

        return queryset.order_by("-article_no").distinct()
