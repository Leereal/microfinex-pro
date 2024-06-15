from django.urls import path
from .views import AllGroupListView, GroupListCreateView, GroupDetailView

urlpatterns = [
    path('', GroupListCreateView.as_view(), name='group-list-create'),
    path('all/', AllGroupListView.as_view(), name='all-group-list'),
    path('<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
]
