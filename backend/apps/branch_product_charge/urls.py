from django.urls import path
from .views import AllBranchProductChargesListView, BranchProductChargeDetailView, BranchProductChargeListCreateView
urlpatterns = [
    path("all/", AllBranchProductChargesListView.as_view(), name="all-branch-product-charges-list"),
    path("", BranchProductChargeListCreateView.as_view(), name="branch-product-charges-list"),
    path("<int:pk>/", BranchProductChargeDetailView.as_view(), name="branch-product-charge-detail"),
]
