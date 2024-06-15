from django.urls import path

from .views import (
    ClientListAPIView,
    ClientDetailAPIView,
)

urlpatterns = [
    path("", ClientListAPIView.as_view(), name="all-clients"),
    path("<int:pk>/", ClientDetailAPIView.as_view(), name="client-detail"),
]
