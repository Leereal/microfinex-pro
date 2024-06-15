from django.urls import path

from .views import (
    ProfileDetailAPIView,
    ProfileListAPIView,
    UpdateProfileAPIView,
)

urlpatterns = [
    path("", ProfileListAPIView.as_view(), name="all-profiles"),
    path("me/", ProfileDetailAPIView.as_view(), name="my-profile"),
    path("me/update/", UpdateProfileAPIView.as_view(), name="update-profile"),
]