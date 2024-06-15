from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from rest_framework import permissions

from .documents import ClientDocument
from .serializers import ClientElasticSearchSerializer


class ClientElasticSearchView(DocumentViewSet):
    document = ClientDocument
    serializer_class = ClientElasticSearchSerializer
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    search_fields = (
        "full_name",
        "last_name",
        "national_id",
        "passport_number",
        "street_number",
        "ip_address",
    )
    filter_fields = {
        "created_at": "created_at",
    }

    ordering_fields = {"created_at": "created_at"}
    ordering = ("-created_at",)