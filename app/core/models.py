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

    def __str__(self):
        return self.article_name
