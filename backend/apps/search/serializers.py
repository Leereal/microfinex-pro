from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .documents import ClientDocument


class ClientElasticSearchSerializer(DocumentSerializer):
    class Meta:
        document = ClientDocument
        fields = [
            'full_name',
            'last_name',
            'national_id',
            'passport_number',
           'street_number',
            'ip_address',
            'created_at',
        ]