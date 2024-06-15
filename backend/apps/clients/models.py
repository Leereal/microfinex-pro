from datetime import datetime
from http import client
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.audits.auditing import AuditableMixin
from django.contrib.postgres.fields import ArrayField
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django_countries import countries

from apps.common.models import TimeStampedModel
from apps.branches.models import Branch
from apps.currencies.models import Currency

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

    branch = models.ForeignKey(Branch, verbose_name=_('Branch'), on_delete=models.SET_NULL, blank=True, null=True, related_name='clients')
    created_by = models.ForeignKey(User, verbose_name=_('Created By'), on_delete=models.SET_NULL, blank=True, null=True)
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
    nationality = models.CharField(_('Nationality'), max_length=255, blank=True, null=True)
    passport_number = models.CharField(_('Passport Number'), max_length=255, unique=True, blank=True, null=True)
    passport_country = models.CharField(verbose_name=_("passport country"), max_length=200, blank=True, null=True, choices=countries)
    photo = models.CharField(_('Photo'), max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(_('Date of Birth'))
    title = models.CharField(_('Title'), max_length=10, choices=Title.choices , blank=True, null=True)
    gender = models.CharField(_('Gender'), max_length=20, choices=Gender.choices, default=Gender.OTHER)
    street_number = models.CharField(_('Street Number'), max_length=255, blank=True, null=True)
    suburb = models.CharField(_('Suburb'), max_length=255, blank=True, null=True)
    zip_code = models.CharField(_('ZIP Code'), max_length=20, blank=True, null=True)
    city = models.CharField(_('City'), max_length=255, blank=True, null=True)
    state = models.CharField(_('State / Province'), max_length=255, blank=True, null=True)
    country = models.CharField(_("Country"), max_length=200, null=True, choices=countries)
    guarantor = models.CharField('self', max_length=255, blank=True, null=True)
    is_guarantor = models.BooleanField(_('Is Guarantor'), default=False)
    status = models.CharField(_('Status'), max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_by = models.ForeignKey(User, verbose_name=_('Created By'), on_delete=models.SET_NULL, blank=True, null=True)
    branch = models.ForeignKey(Branch, verbose_name=_('Branch'), on_delete=models.CASCADE)
    is_active = models.BooleanField(_('Is Active'), default=True)
    ip_address = models.GenericIPAddressField(_('IP Address'), blank=True, null=True)
    device_details = models.TextField(blank=True, null=True)
 
    def get_age(self):
        if self.date_of_birth:
            return int((datetime.now().date() - self.date_of_birth).days / 365.25)
        return None
    
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"
    
    def get_full_address(self):
        return f"{self.street_number} {self.suburb} {self.zip_code} {self.city} {self.state} {self.country}"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
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
    phone = PhoneNumberField(verbose_name=_("phone number"), max_length=30 ) 
    type = models.CharField(_('Contact Type'), max_length=20, choices=ContactType.choices, default=ContactType.OTHER)
    is_primary = models.BooleanField(_('Primary'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)
    whatsapp = models.BooleanField(_('WhatsApp'), default=False)



    @property
    def get_country_code(self):
        return self.phone.country_code
    
    class Meta:
        verbose_name = _("Client Contact")
        verbose_name_plural = _("Client Contacts")
        unique_together = ('client', 'phone')  # Ensure uniqueness of client-phone combination

    def __str__(self):
        return f"{self.client.first_name} {self.client.last_name} - {self.type} - {self.phone}"

    def get_audit_fields(self):
        # Dynamically retrieve all field names from the model
        return [field.name for field in self._meta.fields]
    

class NextOfKin(TimeStampedModel):
    client = models.OneToOneField(Client, verbose_name=_('Client'), related_name='next_of_kin', on_delete=models.CASCADE)
    first_name = models.CharField(_('First Name'), max_length=50)
    last_name = models.CharField(_('Last Name'), max_length=50)
    email = models.EmailField(_('Email'),blank=True,null=True)
    phone = PhoneNumberField(_('Phone Number'), blank=True,null=True)
    relationship = models.CharField(_('Relationship'), max_length=255, blank=True, null=True)
    address = models.TextField(_('Address'), blank=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_('Created By'), on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(_('Is Active'), default=True)

    class Meta:
        verbose_name = _('Next of Kin')
        verbose_name_plural = _('Next of Kin')

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Relationship: {self.relationship})"


class ClientLimit(TimeStampedModel):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name="client_limit")
    max_loan = models.DecimalField(max_digits=15, decimal_places=2)
    credit_score = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def __str__(self):
        return f"Client Limits - ID: {self.id}, Client: {self.client}"