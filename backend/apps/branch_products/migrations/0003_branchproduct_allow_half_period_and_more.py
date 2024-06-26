# Generated by Django 5.0.2 on 2024-03-08 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("branch_products", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="branchproduct",
            name="allow_half_period",
            field=models.BooleanField(default=False, verbose_name="allow half period"),
        ),
        migrations.AddField(
            model_name="branchproduct",
            name="grace_period_days",
            field=models.IntegerField(default=5, verbose_name="grace period in days"),
            preserve_default=False,
        ),
    ]
