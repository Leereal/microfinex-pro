# Generated by Django 5.0.2 on 2024-03-09 11:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("loan_transactions", "0002_alter_loantransaction_loan_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="loantransaction",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created By",
            ),
        ),
        migrations.AlterField(
            model_name="loantransaction",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="A brief description of the transaction.",
                null=True,
                verbose_name="Description",
            ),
        ),
        migrations.AlterField(
            model_name="loantransaction",
            name="transaction_type",
            field=models.CharField(
                choices=[
                    ("disbursement", "Disbursement"),
                    ("repayment", "Repayment"),
                    ("interest", "Interest"),
                    ("charge", "Charge"),
                    ("refund", "Refund"),
                    ("bonus", "Bonus"),
                    ("topup", "Topup"),
                ],
                max_length=20,
                verbose_name="Transaction Type",
            ),
        ),
    ]
