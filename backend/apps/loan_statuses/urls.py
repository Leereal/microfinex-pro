from django.urls import path
from .views import LoanStatusListCreateView, LoanStatusDetailView

urlpatterns = [
    path('', LoanStatusListCreateView.as_view(), name='loan-statuses-list-create'),
    path('<int:pk>/', LoanStatusDetailView.as_view(), name='loan-status-detail'),
]
