from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChargeListCreateView.as_view(), name='charge-list-create'),
    path('<int:pk>/', views.ChargeDetailView.as_view(), name='charge-detail'),
]
