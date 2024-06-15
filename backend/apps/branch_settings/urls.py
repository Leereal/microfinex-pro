from django.urls import path
from .views import BranchSettingsListCreateView, BranchSettingsDetailView

urlpatterns = [
    path('', BranchSettingsListCreateView.as_view(), name='branch-settings-list-create'),
    path('<int:pk>/', BranchSettingsDetailView.as_view(), name='branch-settings-detail'),
]
