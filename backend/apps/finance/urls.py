from django.urls import path
from .views import AllFinanceListView, FinanceListView, FinanceDetailView

urlpatterns = [
    path('all/', AllFinanceListView.as_view(), name='all-finance-list'),
    path('', FinanceListView.as_view(), name='finance-list'),
    path('<int:pk>/', FinanceDetailView.as_view(), name='finance-detail'),
]
