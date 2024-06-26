# Generated by Django 5.0.2 on 2024-03-07 16:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("branches", "0001_initial"),
        ("currencies", "0001_initial"),
        ("loans", "0001_initial"),
        ("payment_gateways", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="LoanTransaction",
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
                    "description",
                    models.TextField(
                        help_text="A brief description of the transaction.",
                        verbose_name="Description",
                    ),
                ),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[
                            ("disbursement", "Disbursement"),
                            ("repayment", "Repayment"),
                            ("interest", "Interest"),
                            ("charge", "Charge"),
                            ("refund", "Refund"),
                        ],
                        max_length=20,
                        verbose_name="Transaction Type",
                    ),
                ),
                (
                    "debit",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Amount debited (if applicable).",
                        max_digits=15,
                        null=True,
                        verbose_name="Debit Amount",
                    ),
                ),
                (
                    "credit",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Amount credited (if applicable).",
                        max_digits=15,
                        null=True,
                        verbose_name="Credit Amount",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("review", "Review"),
                            ("pending", "Pending"),
                            ("approved", "Approved"),
                            ("cancelled", "Cancelled"),
                            ("refunded", "Refund"),
                        ],
                        max_length=20,
                        verbose_name="Transaction Status",
                    ),
                ),
                (
                    "branch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="branches.branch",
                        verbose_name="Branch",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "currency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="currencies.currency",
                        verbose_name="Currency",
                    ),
                ),
                (
                    "loan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="loans.loan",
                        verbose_name="Loan",
                    ),
                ),
                (
                    "payment_gateway",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="payment_gateways.paymentgateway",
                        verbose_name="Payment Gateway",
                    ),
                ),
            ],
            options={
                "verbose_name": "Loan Transaction",
                "verbose_name_plural": "Loan Transactions",
            },
        ),
    ]
