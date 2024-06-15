from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from apps.clients.models import Client
from apps.common.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()

class Employer(TimeStampedModel):
    client = models.OneToOneField(Client, verbose_name=_('Client'), on_delete=models.CASCADE, related_name='employer', blank=True, null=True)
    contact_person = models.CharField(_('Contact Person'), max_length=255, blank=True, null=True)
    email = models.EmailField(_('Email'), max_length=255, blank=True, null=True)
    phone = PhoneNumberField(_('Phone Number'), blank=True, null=True)
    name = models.CharField(_('Name'), max_length=255)
    address = models.TextField(_('Address'), blank=True, null=True)
    employment_date = models.DateField(_('Employment Date'), blank=True, null=True)
    job_title = models.CharField(_('Job Title'), max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, verbose_name=_('Created By'), on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(_('Is Active'), default=True)

    class Meta:
        verbose_name = _('Employer')
        verbose_name_plural = _('Employers')

    def __str__(self):
        return self.name 