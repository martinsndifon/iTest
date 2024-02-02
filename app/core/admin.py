"""
Django admin customization
"""
from django.contrib import admin

from core import models

admin.site.register(models.Provider)
admin.site.register(models.Article)
