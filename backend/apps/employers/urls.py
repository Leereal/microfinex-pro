from django.urls import path
from .views import EmployerListView, EmployerDetailView

urlpatterns = [
    path('', EmployerListView.as_view(), name='employer-list'),
    path('<int:pk>/', EmployerDetailView.as_view(), name='employer-detail'),
]
