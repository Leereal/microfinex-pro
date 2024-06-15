from django.urls import path
from .views import CurrencyListAPIView, CurrencyDetailAPIView

urlpatterns = [
    path('', CurrencyListAPIView.as_view(), name='currency-list'),
    path('<int:pk>/', CurrencyDetailAPIView.as_view(), name='currency-detail'),
]
