from django.urls import path
from .views import PeriodListCreateView, PeriodDetailView

urlpatterns = [
    path('', PeriodListCreateView.as_view(), name='period-list-create'),
    path('<int:pk>/', PeriodDetailView.as_view(), name='period-detail'),
]
