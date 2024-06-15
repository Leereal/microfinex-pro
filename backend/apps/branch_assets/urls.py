from django.urls import path
from .views import BranchAssetsListCreateAPIView, BranchAssetsRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', BranchAssetsListCreateAPIView.as_view(), name='branch-assets-list-create'),
    path('<int:pk>/', BranchAssetsRetrieveUpdateDestroyAPIView.as_view(), name='branch-assets-detail'),
]
