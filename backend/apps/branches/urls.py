from django.urls import path
from .views import BranchListAPIView, BranchDetailAPIView

urlpatterns = [
    path("", BranchListAPIView.as_view(), name="branch-list"),
    path("<int:pk>/", BranchDetailAPIView.as_view(), name="branch-detail"),
]
