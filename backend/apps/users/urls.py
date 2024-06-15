from django.urls import path

from .views import UserBranchView

urlpatterns = [
    path("user-branch/", UserBranchView.as_view(), name="delete-userbranch")
]
