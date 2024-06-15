# Generated by Django 5.0.2 on 2024-03-06 03:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0004_clientlimit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clientlimit",
            name="client",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="client_limit",
                to="clients.client",
            ),
        ),
    ]