from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='clients.get_full_name', read_only=True)   
    document_type_name = serializers.CharField(source='document_types.name', read_only=True)
    uploaded_by = serializers.CharField(source='users.get_full_name', read_only=True)
    branch_name = serializers.CharField(source='branches.name', read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'client','client_name','document_type_name','uploaded_by','branch_name', 'loan', 'name', 'file', 'document_type', 'branch']
        read_only_fields = ['id']

