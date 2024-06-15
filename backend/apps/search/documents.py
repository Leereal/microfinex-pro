from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from apps.clients.models import Client

@registry.register_document
class ClientDocument(Document):
    full_name = fields.TextField(attr='first_name')
    last_name = fields.TextField(attr='last_name')
    national_id = fields.TextField(attr='national_id')
    passport_number = fields.TextField(attr='passport_number')
    street_number = fields.TextField(attr='street_number')
    ip_address = fields.TextField(attr='ip_address')

    class Index:
        name = 'clients'
        settings = {"number_of_shards":1, "number_of_replicas":0}

    class Django:
        model = Client
        fields = ["created_at"]

    def prepare_client_first_name(self, instance):
        return instance.client.first_name

    def prepare_client_last_name(self, instance):
        return instance.client.last_name
        