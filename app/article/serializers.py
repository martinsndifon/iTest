"""
Serializers for article APIs.
"""
from rest_framework import serializers
from core.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for article objects."""

    class Meta:
        model = Article
        fields = [
            "article_no",
            "article_name",
            "price",
            "provider_no",
        ]
        read_only_fields = ["article_no"]

    def validate(self, data):
        if "article_name" in data and "price" in data and "provider_no" in data:
            # Ensure the combination of article_name, price, and provider_no is unique
            if Article.objects.filter(
                article_name=data["article_name"],
                price=data["price"],
                provider_no=data["provider_no"],
            ).exists():
                raise serializers.ValidationError(
                    "Article with the same name, price, and provider already exists."
                )
        return data
