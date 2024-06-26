# Generated by Django 5.0.2 on 2024-03-05 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Currency",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("name", models.CharField(max_length=255, unique=True)),
                ("code", models.CharField(max_length=10, unique=True)),
                ("symbol", models.CharField(max_length=10, unique=True)),
                ("position", models.CharField(default="before", max_length=10)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "currency",
                "verbose_name_plural": "currencies",
            },
        ),
    ]
