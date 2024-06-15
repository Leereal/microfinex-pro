from django.urls import path
from .views import AllGroupProductChargesListView, GroupProductChargeDetailView, GroupProductChargeListCreateView

urlpatterns = [
    path("all/", AllGroupProductChargesListView.as_view(), name="all-group-product-charges-list"),
    path("", GroupProductChargeListCreateView.as_view(), name="group-product-charges-list"),
    path("<int:pk>/", GroupProductChargeDetailView.as_view(), name="group-product-charge-detail"),
]
