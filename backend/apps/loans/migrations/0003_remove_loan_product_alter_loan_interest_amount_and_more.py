# Generated by Django 5.0.2 on 2024-03-09 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("loans", "0002_rename_repayment_date_loan_expected_repayment_date_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="loan",
            name="product",
        ),
        migrations.AlterField(
            model_name="loan",
            name="interest_amount",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text="The total amount of interest applied to the loan.",
                max_digits=15,
                null=True,
                verbose_name="Interest Amount",
            ),
        ),
        migrations.AlterField(
            model_name="loan",
            name="interest_rate",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text="The interest rate of the loan.",
                max_digits=10,
                null=True,
                verbose_name="Interest Rate",
            ),
        ),
    ]