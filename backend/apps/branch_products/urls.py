from django.urls import path
from .views import AllBranchProductListView, BranchProductListCreateView, BranchProductDetailView

urlpatterns = [
    path('all/', AllBranchProductListView.as_view(), name='all-branch-products'),
    path('', BranchProductListCreateView.as_view(), name='branch-product-list-create'),
    path('<int:pk>/', BranchProductDetailView.as_view(), name='branch-product-detail'),
]
