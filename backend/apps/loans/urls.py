from django.urls import path
from .views import AllLoansListView,  LoanListCreateView, LoanDetailView, LoanPaymentView, LoanPaymentsView, ManageLoanView
urlpatterns = [
    # Paths for Client operations
    path('all/', AllLoansListView.as_view(), name='loan-list'),
    path('', LoanListCreateView.as_view(), name='loan-create-list'),
    path('<int:pk>/', LoanDetailView.as_view(), name='loan-detail'),
    path('<int:pk>/manage/', ManageLoanView.as_view(), name='manage-loan'),
    path('<int:pk>/payments/', LoanPaymentView.as_view(), name='loan-repayment'),
    path('<int:pk>/payments/history/', LoanPaymentsView.as_view(), name='loan-payments-history'),
]