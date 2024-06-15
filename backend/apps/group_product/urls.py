from django.urls import path
from .views import (
    AllGroupProductListView,
    GroupProductListCreateView,
    GroupProductDetailView,
)

urlpatterns = [
    path('', GroupProductListCreateView.as_view(), name='group-product-list-create'),
    path('all/', AllGroupProductListView.as_view(), name='all-group-product-list'),
    path('<int:pk>/', GroupProductDetailView.as_view(), name='group-product-detail'),
]
