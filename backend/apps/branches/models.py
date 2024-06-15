from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django_countries import countries
from phonenumber_field.modelfields import PhoneNumberField
from apps.audits.auditing import AuditableMixin
from apps.common.models import TimeStampedModel
from django.core.validators import MinLengthValidator

class Branch(AuditableMixin, TimeStampedModel):  # Inherit from AuditableMixin
    name = models.CharField(verbose_name=_("name"), max_length=255, validators=[MinLengthValidator(3)])
    address = models.TextField(verbose_name=_("address"), max_length=255, blank=True)
    email = models.EmailField(verbose_name=_("email address"), default=None, blank=True)
    phone = PhoneNumberField(
        verbose_name=_("phone number"), max_length=30, default=None, blank=True
    )
    is_active = models.BooleanField(verbose_name=_("is active"),default=True)
    country = models.CharField(verbose_name=_("country"), max_length=200, null=True, choices=countries)


    class Meta:
        verbose_name = _("branch")
        verbose_name_plural = _("branches")

    def __str__(self):
        return self.name

    
    def average_loan(self): # We can also include this to branch serializer
        #We are getting all loans based on the relationship related_name in branch_loans model
        loans = self.branch_loans.all()
        if loans.count() > 0:
            # let's iterate through each loan and get the amount then sum them
            total_loans = sum(loan.amount for loan in loans)
            average_loan = total_loans / loans.count()
            return round(average_loan,2)
        return None

    def get_audit_fields(self):
        # Override the get_audit_fields method to specify fields to audit
        return ['name', 'address', 'email', 'phone', 'is_active', 'country']
