from os import read
from rest_framework import serializers
# from apps.loans.models import Loan
# from apps.loans.serializers import LoanSerializer

# from apps.next_of_kins.serializers import NextOfKinSerializer
from .models import Client, Contact
from rest_framework.exceptions import ValidationError

#To handle multiple values we use this
class ContactListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        contact_mapping = {contact.id: contact for contact in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for contact_id, data in data_mapping.items():
            contact = contact_mapping.get(contact_id, None)
            if contact is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(contact, data))

        # Perform deletions.
        for contact_id, contact in contact_mapping.items():
            if contact_id not in data_mapping:
                contact.delete()

        return ret


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['country_code', 'phone', 'type', 'is_primary','is_active','whatsapp']
        list_serializer_class = ContactListSerializer

class ClientSerializer(serializers.ModelSerializer):
#     loans = serializers.SerializerMethodField()
#     loans_count = serializers.SerializerMethodField()
#     loan_applications = serializers.StringRelatedField(many=True, read_only=True)
#     contacts = ContactListSerializer(many=True)
#     next_of_kin = NextOfKinSerializer(required=False)
#     average_loan = serializers.ReadOnlyField()

#     def get_average_loan(self,obj):
#         return obj.average_loan()
    
#     #Keep this. We 
#     def get_loans(self,obj):
#         loans = Loan.objects.filter(client=obj)
#         return LoanSerializer(loans, many=True).data
    
#     def get_loans_count(self,obj):
#         return Loan.objects.filter(client=obj).count() 
    
    class Meta:
        model = Client
        fields = [
            "id",
            "first_name",
            "last_name",
            "emails",
            "national_id",
            "nationality",
            "passport_number",
            "passport_country",
            "photo",
            "date_of_birth",
            "title",
            "gender",
            "street_number",
            "suburb",
            "zip_code",
            "city",
            "state",
            "country",
            "guarantor",
            "is_guarantor",
            "status",
            "created_by",
            "branch",
            "is_active",
            "ip_address",
            "device_details",
        #     "loans",
        #     "loans_count",
        #     "loan_applications",
        #     "contacts",
        #     "next_of_kin",
        #     "average_loan"
        ]

#     def create(self, validated_data):
#         # contacts_data = validated_data.pop('contacts')
#         next_of_kin_data = validated_data.pop('next_of_kin',None)
#         client = Client.objects.create(**validated_data)
        
#         # Save contacts and atleast one contact is required
#         if contacts_data:
#             for contact_data in contacts_data:
#                 Contact.objects.create(client=client, **contact_data)
#         else:
#             raise ValidationError("Contacts data is required.")
        
#         if next_of_kin_data:
#             NextOfKinSerializer.create(NextOfKinSerializer(), next_of_kin_data, client)

#         return client

class UpdateClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "emails",
            "national_id",
            "nationality",
            "passport_number",
            "passport_country",
            "photo",
            "date_of_birth",
            "title",
            "gender",
            "street_number",
            "suburb",
            "zip_code",
            "city",
            "state",
            "country",
            "guarantor",
            "is_guarantor",
            "status",
            "branch",
            "is_active",
            "ip_address",
            "device_details",
        ]
    
    # def update(self, instance, validated_data):
    #     request = self.context.get('request')

    #     # Check if the request was performed by user or contains user.
    #     if not request or not request.user:
    #         # Raise error or if use default user null / something
    #         raise ValidationError("Request or user not found in context.")
    #     print("User : ",request.user)
    #     #Add the user to the validated data
    #     validated_data['created_by'] = request.user
        

    #     return super().update(instance, validated_data)
