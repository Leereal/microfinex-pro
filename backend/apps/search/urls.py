from django.urls import path

from .views import ClientElasticSearchView

urlpatterns = [
    path(
        "search/",
        ClientElasticSearchView.as_view({"get": "list"}),
        name="client_search",
    )
]