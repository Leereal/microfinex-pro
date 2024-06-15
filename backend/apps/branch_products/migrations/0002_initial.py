# Generated by Django 5.0.2 on 2024-03-05 05:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("branch_products", "0001_initial"),
        ("periods", "0001_initial"),
        ("products", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="branchproduct",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="created by",
            ),
        ),
        migrations.AddField(
            model_name="branchproduct",
            name="period",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="periods.period",
                verbose_name="loan period",
            ),
        ),
        migrations.AddField(
            model_name="branchproduct",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="products.product",
                verbose_name="product",
            ),
        ),
    ]
