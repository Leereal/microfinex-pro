# Generated by Django 5.0.2 on 2024-03-06 13:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("loan_statuses", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="loanstatus",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="loanstatus",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="loanstatus",
            name="last_modified",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
