# Generated by Django 4.0.10 on 2024-02-01 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_name',
            field=models.CharField(max_length=255),
        ),
    ]
