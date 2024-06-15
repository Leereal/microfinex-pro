from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from apps.branch_products.models import BranchProduct
from apps.branch_settings.models import BranchSettings

from apps.clients.models import Client, ClientLimit
from apps.global_settings.models import GlobalSettings
from apps.group_product.models import GroupProduct


def validate_loan_amount(value, client, context):
    """
    Validates the loan amount.

    This function ensures that the loan amount does not exceed the client's maximum loan limit (if applicable)
    and falls within the allowed range defined by global, branch-specific, and group-specific settings.

    Args:
        value (Decimal): The loan amount to be validated.
        client (Client): The client object associated with the loan.
        context (dict): The context of the serializer.

    Returns:
        Decimal: The validated loan amount.

    Raises:
        serializers.ValidationError: If the loan amount exceeds the client's maximum loan limit,
            or if it falls outside the allowed range.
    """
    # Check if the client has a maximum loan limit
    client_max_loan = None

    if client:
        try:
            client_limit = ClientLimit.objects.get(client=client)
            client_max_loan = client_limit.max_loan
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f"Client {client} does not have a Client Limit.")

    # Validate loan amount against client's maximum loan limit
    if client_max_loan is not None and value > client_max_loan:
        raise serializers.ValidationError(f"Loan amount exceeds client's maximum loan limit of {client_max_loan}.")

    # Fetch global settings for loan amount range
    global_settings = GlobalSettings.objects.first()

    # Determine branch-specific settings (if available)
    branch_settings = (
        BranchSettings.objects.filter(branch=context.get('request').user.active_branch).first()
        if context.get('request')
        else None
    )

    # Determine group-specific settings (if available)
    group_settings = None
    branch_product_settings = None
    group_product = context.get('group_product')
    branch_product = context.get('branch_product')

    if group_product:
        try:
            group_product_instance = GroupProduct.objects.get(pk=group_product)
            group_settings = group_product_instance
        except ObjectDoesNotExist:
            pass

    if branch_product:
        try:
            branch_product_instance = BranchProduct.objects.get(pk=branch_product)
            branch_product_settings = branch_product_instance
        except ObjectDoesNotExist:
            pass

    # Calculate min and max allowed loan amounts based on precedence
    if group_settings and group_settings.max_amount is not None and group_settings.min_amount is not None:
        min_amount = group_settings.min_amount
        max_amount = group_settings.max_amount
        
    elif branch_product_settings and branch_product_settings.max_amount is not None and branch_product_settings.min_amount is not None:
        min_amount = branch_product_settings.min_amount
        max_amount = branch_product_settings.max_amount

    elif branch_settings and branch_settings.max_loan_amount is not None and branch_settings.min_loan_amount is not None:
        min_amount = branch_settings.min_loan_amount
        max_amount = branch_settings.max_loan_amount
    else:
        min_amount = global_settings.min_loan_amount
        max_amount = global_settings.max_loan_amount

    # Validate loan amount against allowed range
    if not (min_amount <= value <= max_amount):
        raise serializers.ValidationError(f"Amount must be between {min_amount} and {max_amount}.")
    return value

def validate_client(client, branch):
    """
    Validates the client for loan application.

    Args:
        client (Client): The client object associated with the loan.
        branch (Branch): The branch object associated with the loan.

    Raises:
        serializers.ValidationError: If the client is not active,
            or not allowed to get a loan at the moment,
            or does not belong to the same branch as the loan.
    """
    if not client.is_active:
        raise serializers.ValidationError({"client": "Client is not active."})

    if client.status != Client.Status.ACTIVE:
        raise serializers.ValidationError({"client": "Client is not allowed to get a loan at the moment."})

    # Ensure the client belongs to the same branch as the loan, if applicable
    if branch and client.branch != branch:
        raise serializers.ValidationError({"client": "Client is not from this branch."})
