from django.db import models
from apps.branches.models import Branch
from apps.clients.models import Client
from apps.common.models import TimeStampedModel
from apps.document_types.models import DocumentType
from apps.loans.models import Loan
from django.contrib.auth import get_user_model

User = get_user_model()

class Document(TimeStampedModel):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    loan = models.ForeignKey(Loan, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    document_type = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    expiration_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name
