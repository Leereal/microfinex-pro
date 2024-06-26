# Generated by Django 5.0.2 on 2024-03-05 05:47

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("branches", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BranchAssets",
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
                (
                    "item",
                    models.CharField(
                        max_length=255,
                        validators=[django.core.validators.MinLengthValidator(3)],
                        verbose_name="item",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default=None, null=True, verbose_name="description"
                    ),
                ),
                (
                    "brand",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=255,
                        null=True,
                        verbose_name="brand",
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        blank=True, default=None, max_length=50, null=True
                    ),
                ),
                ("quantity", models.IntegerField(default=1, verbose_name="quantity")),
                (
                    "purchase_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="purchase date"
                    ),
                ),
                (
                    "images",
                    models.JSONField(
                        blank=True, default=list, null=True, verbose_name="images"
                    ),
                ),
                (
                    "branch",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="branch_assets",
                        to="branches.branch",
                    ),
                ),
            ],
            options={
                "verbose_name": "branch",
                "verbose_name_plural": "branches",
            },
        ),
    ]
