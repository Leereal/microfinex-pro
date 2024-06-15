from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import TimeStampedModel

User = get_user_model()


class Profile(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = (
            "male",
            _("Male"),
        )

        FEMALE = (
            "female",
            _("Female"),
        )
        OTHER = (
            "other",
            _("Other"),
        )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = PhoneNumberField(verbose_name=_("phone number"), max_length=30, default=None, blank=True, null=True ) 
    gender = models.CharField(
        verbose_name=_("gender"),
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=20,
    )   
    profile_photo = models.ImageField(
        verbose_name=_("profile photo"), default=None, blank=True, null=True
    ) 

    def __str__(self):
        return f"{self.user.first_name}'s Profile"