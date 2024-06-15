from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from apps.audits.auditing import AuditableMixin

from apps.branches.models import Branch
from apps.common.models import TimeStampedModel

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(verbose_name=_("first name"), max_length=50, validators=[MinLengthValidator(3)])
    last_name = models.CharField(verbose_name=_("last name"), max_length=50, validators=[MinLengthValidator(3)])
    email = models.EmailField(
        verbose_name=_("email address"), db_index=True, unique=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    active_branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='active_users')
    date_joined = models.DateTimeField(null=True, blank=True)
    branches = models.ManyToManyField(Branch, through="UserBranch",  through_fields=('user', 'branch'), related_name='users')  

    #so as to use the email as auth
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        permissions =[
            ("ban_user","Can Ban User"),
        ]
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.first_name

    #Property decorator helps us to get the full name not as function e.g user.get_full_name
    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    @property
    def get_short_name(self):
        return f"{self.first_name[:3]} {self.last_name[:3]}"
    
    # def get_audit_fields(self):
    #     # Dynamically retrieve all field names from the model
    #     return ['first_name', 'last_name', 'email', 'is_staff', 'is_active', 'active_branch', 'date_joined', 'branches']
    

class UserBranch(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_branches')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_user')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_user_branches')

    class Meta:
        verbose_name = _("userbranch")
        verbose_name_plural = _("User Branch") 
        unique_together = ('user', 'branch')  # Ensure uniqueness of user-branch combination

    def __str__(self):
        return f"{self.user.first_name} assigned to  {self.branch.name} branch"
    
    # def get_audit_fields(self):
    #     # Dynamically retrieve all field names from the model
    #     return [field.name for field in self._meta.fields]
    
