from django.urls import path
from .views import GlobalSettingsListCreateView, GlobalSettingsDetailView

urlpatterns = [
    path('', GlobalSettingsListCreateView.as_view(), name='global-settings-list-create'),
    path('<int:pk>/', GlobalSettingsDetailView.as_view(), name='global-settings-detail'),
]
