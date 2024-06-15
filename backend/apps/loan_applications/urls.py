from django.urls import path
from .views import (
    AllLoanApplicationsListView,
    LoanApplicationListView,
    LoanApplicationDetailView,
    RejectionReasonListView,
    RejectionReasonDetailView,
)

urlpatterns = [
    path('loan-applications/all/', AllLoanApplicationsListView.as_view(), name='all-loan-applications'),
    path('loan-applications/', LoanApplicationListView.as_view(), name='loan-applications-list'),
    path('loan-applications/<int:pk>/', LoanApplicationDetailView.as_view(), name='loan-application-detail'),
    path('rejection-reasons/', RejectionReasonListView.as_view(), name='rejection-reasons-list'),
    path('rejection-reasons/<int:pk>/', RejectionReasonDetailView.as_view(), name='rejection-reason-detail'),
]
