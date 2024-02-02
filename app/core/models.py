"""
Database Models.
"""
from django.db import models


class Provider(models.Model):
    """
    Provider Model.
    """

    provider_no = models.BigAutoField(primary_key=True)
    provider_name = models.CharField(max_length=255, unique=True)

    class Meta:
        indexes = [
            models.Index(fields=["provider_no"]),
            models.Index(fields=["provider_name"]),
            models.Index(fields=["provider_no", "provider_name"]),
        ]

    def __str__(self):
        return self.provider_name


class Article(models.Model):
    """
    Article Model.
    """

    article_no = models.BigAutoField(primary_key=True)
    article_name = models.CharField(max_length=255)
    price = models.IntegerField(null=False, blank=False)
    provider_no = models.ForeignKey(Provider, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=["article_no"]),
            models.Index(fields=["article_no", "price"]),
            models.Index(fields=["price"]),
            models.Index(fields=["provider_no"]),
        ]

    def __str__(self):
        return self.article_name
