from django.db import models
from apps.clients.models import Client
from apps.loan_transactions.models import LoanTransaction
from apps.loans.models import Loan
from django.contrib.auth import get_user_model
from apps.common.models import TimeStampedModel

User = get_user_model()

class Note(TimeStampedModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    transaction = models.ForeignKey(LoanTransaction, on_delete=models.CASCADE)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Note ID: {self.id}, Client: {self.client}, Loan: {self.loan}"

