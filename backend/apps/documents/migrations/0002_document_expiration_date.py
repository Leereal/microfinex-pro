# Generated by Django 5.0.2 on 2024-03-14 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="expiration_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
