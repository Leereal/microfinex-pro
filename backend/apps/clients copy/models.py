from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import ArrayField
from django_countries.fields import CountryField
from apps.audits.auditing import AuditableMixin

from apps.common.models import TimeStampedModel
from apps.branches.models import Branch

User = get_user_model()

class Client(AuditableMixin,TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = 'male', _('Male')
        FEMALE = 'female', _('Female')
        OTHER = 'other', _('Other')

    class Status(models.TextChoices):
        ACTIVE = 'active', _('Active')
        BANNED = 'banned', _('Banned')
        RESTRICTED = 'restricted', _('Restricted')
        DIED = 'died', _('Died')

    class Title(models.TextChoices):
        DR = 'Dr', _('Dr')
        MISS = 'Miss', _('Miss')
        MR = 'Mr', _('Mr')
        MRS = 'Mrs', _('Mrs')
        MS = 'Ms', _('Ms')
        PROF = 'Prof', _('Prof')

    first_name = models.CharField(_('First Name'), max_length=50)
    last_name = models.CharField(_('Last Name'), max_length=50)
    emails = ArrayField(
        models.EmailField(_('Email')), 
        blank=True, 
        null=True,
        default=list,  # Default value is an empty list
        verbose_name=_('Emails')
    )
    national_id = models.CharField(_('National ID'), max_length=255,unique=True, blank=True, null=True)
    nationality = models.CharField(_('Nationality'), max_length=255)
    passport_number = models.CharField(_('Passport Number'), max_length=255, unique=True, blank=True, null=True)
    passport_country = models.CharField(verbose_name=_("passport country"),max_length=200,  null=True, choices=CountryField().choices + [('', 'Select Country')])
    photo = models.CharField(_('Photo'), max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(_('Date of Birth'), blank=True, null=True)
    title = models.CharField(_('Title'), max_length=10, choices=Title.choices)
    gender = models.CharField(_('Gender'), max_length=20, choices=Gender.choices, default=Gender.OTHER)
    street_number = models.CharField(_('Street Number'), max_length=255, blank=True, null=True)
    suburb = models.CharField(_('Suburb'), max_length=255, blank=True, null=True)
    zip_code = models.CharField(_('ZIP Code'), max_length=20, blank=True, null=True)
    city = models.CharField(_('City'), max_length=255, blank=True, null=True)
    state = models.CharField(_('State / Province'), max_length=255)
    country = models.CharField(verbose_name=_("country"),max_length=200,  null=True, choices=CountryField().choices + [('', 'Select Country')])
    guarantor = models.CharField(_('Guarantor'), max_length=255, blank=True, null=True)
    is_guarantor = models.BooleanField(_('Is Guarantor'), default=False)
    status = models.CharField(_('Status'), max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_by = models.ForeignKey(User, verbose_name=_('Created By'), on_delete=models.SET_NULL, blank=True, null=True)
    branch = models.ForeignKey(Branch, verbose_name=_('Branch'), on_delete=models.CASCADE)
    is_active = models.BooleanField(_('Is Active'), default=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    device_details = models.TextField(blank=True, null=True)

    
    

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')
    
    def clean(self):
        """
        Validate that if passport_number is not null, then passport_country must also not be null.
        """
        if not self.national_id and not self.passport_number:
            raise ValidationError({
                'national_id': _('National ID or Passport Number must be provided.'),
                'passport_number': _('National ID or Passport Number must be provided.')
            })
        
        if self.passport_number and not self.passport_country:
            raise ValidationError({'passport_country': _('Passport Country must be provided if Passport Number is specified.')})
    
    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

        # Capture IP address and device details before saving
        if self.pk and 'request' in kwargs:
            request = kwargs.pop('request')
            self.ip_address = request.META.get('REMOTE_ADDR', None)
            user_agent = request.META.get('HTTP_USER_AGENT', None)
            if user_agent:
                self.device_details = user_agent
            if not self.created_by and request.user.is_authenticated:
                self.created_by = request.user

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.title.title()} {self.first_name.title()} {self.last_name.title()}"
    
    def average_loan(self): # We can also include this to client serializer
        #We are getting all loans based on the relationship related_name in loans model
        loans = self.loans.all()
        if loans.count() > 0:
            # let's iterate through each loan and get the amount then sum them
            total_loans = sum(loan.amount for loan in loans)
            average_loan = total_loans / loans.count()
            return round(average_loan,2)
        return None

    def get_audit_fields(self):
        # Dynamically retrieve all field names from the model
        return [field.name for field in self._meta.fields]





class Contact(models.Model):
    class ContactType(models.TextChoices):
        CELLPHONE = 'Cellphone', _('Cellphone')
        HOME = 'Home', _('Home')
        WORK = 'Work', _('Work')
        OTHER = 'Other', _('Other')

    client = models.ForeignKey(Client, verbose_name=_('Client'), related_name='contacts', on_delete=models.CASCADE)
    country_code = models.CharField(_('Country Code'), max_length=5)
    phone = PhoneNumberField(verbose_name=_("phone number"), max_length=30, default=None, blank=True, null=True ) 
    type = models.CharField(_('Contact Type'), max_length=20, choices=ContactType.choices, default=ContactType.OTHER)
    is_primary = models.BooleanField(_('Primary'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)
    whatsapp = models.BooleanField(_('WhatsApp'), default=False)

    def save(self, *args, **kwargs):
        if not self.client_id:
            raise ValueError("Client instance must have a primary key value before creating a contact.")

        super().save(*args, **kwargs)
        
        if not self.client.contacts.exists():
            raise ValidationError('At least one contact must be provided for the client.')
    
    def get_audit_fields(self):
        # Dynamically retrieve all field names from the model
        return [field.name for field in self._meta.fields]