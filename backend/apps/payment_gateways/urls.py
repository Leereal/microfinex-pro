from django.urls import path
from .views import PaymentGatewayListCreateView, PaymentGatewayDetailView

urlpatterns = [
    path('', PaymentGatewayListCreateView.as_view(), name='payment-gateway-list'),
    path('<int:pk>/', PaymentGatewayDetailView.as_view(), name='payment-gateway-detail'),
]
