from django.urls import path
from .views import AuditLogListAPIView, AuditLogDetailAPIView

urlpatterns = [
    path('', AuditLogListAPIView.as_view(), name='audit-log-list'),
    path('<int:pk>/', AuditLogDetailAPIView.as_view(), name='audit-log-detail'),
]
