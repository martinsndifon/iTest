# Generated by Django 4.0.10 on 2024-02-01 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('provider_no', models.BigAutoField(primary_key=True, serialize=False)),
                ('provider_name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('article_no', models.BigAutoField(primary_key=True, serialize=False)),
                ('article_name', models.CharField(max_length=255, unique=True)),
                ('price', models.IntegerField()),
                ('provider_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.provider')),
            ],
        ),
    ]