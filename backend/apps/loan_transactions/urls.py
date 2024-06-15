from django.urls import path
from .views import AddChargeView, AllTransactions, RefundView, BonusView, TopUpView

urlpatterns = [
    path('all/', AllTransactions.as_view(), name='all-transactions'),
    path('add-charge/', AddChargeView.as_view(), name='add-charge'),
    path('refund/', RefundView.as_view(), name='refund'),
    path('bonus/', BonusView.as_view(), name='bonus'),
    path('top-up/', TopUpView.as_view(), name='top-up'),
]
