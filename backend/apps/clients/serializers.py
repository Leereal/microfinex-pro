from datetime import timedelta
from http import client
from tkinter import E
from django.utils.timezone import now
from rest_framework import serializers
from apps.employers.models import Employer

from apps.employers.serializers import EmployerSerializer

from .models import Client, Contact, NextOfKin, ClientLimit
from django_countries.serializer_fields import CountryField

class ClientLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientLimit
        fields = ('id', 'client', 'max_loan', 'credit_score', 'currency')

    def validate_max_loan(self, value):
        """
        Check that the max_loan is a positive number.
        """
        if value < 0:
            raise serializers.ValidationError("Max Loan must be a positive number.")
        return value
    
    def validate_credit_score(self, value):
        """
        Check that the credit_score is a positive number.
        """
        if value < 0:
            raise serializers.ValidationError("Credit Score must be a positive number.")
        return value

    def validate(self, data):
        """
        Perform custom validation to ensure that the client has only one ClientLimit instance.
        """
        client = data.get('client')
        if client and ClientLimit.objects.filter(client=client).exists():
            raise serializers.ValidationError("Client already has a Client Limit.")
        return data

class NextOfKinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextOfKin
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'relationship', 'address', 'created_by', 'is_active')

class ContactSerializer(serializers.ModelSerializer):
    #Explicitly add id like this to allow for updates and delete without this it won't work properly
    id = serializers.IntegerField(allow_null=True, required=False)
    country_code = serializers.ReadOnlyField(source='get_country_code')
    client = serializers.PrimaryKeyRelatedField(read_only=True)    
    
    class Meta:
        model = Contact
        fields = ('id', 'client', 'phone', 'type', 'is_primary', 'is_active', 'whatsapp', 'country_code')
        extra_kwargs = {'client': {'read_only': True}} 

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['country_code'] = instance.get_country_code
        return representation


class ClientSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, required=False)  # Assuming at least one contact is required
    country = CountryField(name_only=True) 
    passport_country = CountryField(name_only=True)   
    next_of_kin = NextOfKinSerializer()
    employer = EmployerSerializer()
    client_limit = ClientLimitSerializer()
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = Client
        fields = '__all__'  # Or list specific fields you want to include
   
    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts', [])
        next_of_kin_data = validated_data.pop('next_of_kin')
        employer_data = validated_data.pop('employer')
        client_limit_data = validated_data.pop('client_limit')

        client = Client.objects.create(**validated_data)
        
        if next_of_kin_data:            
            NextOfKin.objects.create(client=client, **next_of_kin_data)
        
        if employer_data:
            Employer.objects.create(client=client, **employer_data)
        
        if client_limit_data:
            ClientLimit.objects.create(client=client, **client_limit_data)
        
        for contact_data in contacts_data:
            Contact.objects.create(client=client, **contact_data)

        # No need to call update_or_create here as the client is already created and associated correctly
        
        return client
    
    def update(self, instance, validated_data):
        contacts_data = validated_data.pop('contacts', [])
        next_of_kin_data = validated_data.pop('next_of_kin', None)
        employer_data = validated_data.pop('employer', None)
        client_limit_data = validated_data.pop('client_limit', None)

        # Update the Client instance attributes
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create Next of Kin
        if next_of_kin_data:
            NextOfKin.objects.update_or_create(client=instance, defaults=next_of_kin_data)
        
        # Update or create Employer
        if employer_data:
            Employer.objects.update_or_create(client=instance, defaults=employer_data)

        # Update or create Client Limit
        if client_limit_data:
            ClientLimit.objects.update_or_create(client=instance, defaults=client_limit_data)
        
        # Existing contact IDs for the client
        existing_contact_ids = set(instance.contacts.all().values_list('id', flat=True))
        processed_contact_ids = set()

        for contact_data in contacts_data:           
            contact_id = contact_data.get('id')
            # Existing contact update
            if contact_id and contact_id in existing_contact_ids:
                Contact.objects.filter(id=contact_id).update(**contact_data)
                processed_contact_ids.add(contact_id)
            else:
                # Skip creation if the phone number already exists for this client
                phone = contact_data.get('phone')
                if not Contact.objects.filter(client=instance, phone=phone).exists():
                    Contact.objects.create(client=instance, **contact_data)
                # Note: If the phone number exists, we do nothing (i.e., we skip)

        # Delete contacts not in the updated data
        contacts_to_delete = existing_contact_ids - processed_contact_ids
        if contacts_to_delete:
            Contact.objects.filter(id__in=contacts_to_delete).delete()

        return instance





    def get_age(self, obj):
        return obj.get_age()
    
    def get_country_name(self, obj):
        return obj.country.name
     
    def validate_date_of_birth(self, value):
        """
        Check that the client is at least 18 years old.
        """
        age = now().date() - value
        if age < timedelta(days=18*365.25):  # Approximation for leap years
            raise serializers.ValidationError("Client must be at least 18 years old.")
        return value
    
    def validate_passport_number(self, value):
        """
        Check that the passport number is unique if provided and not empty, 
        excluding the current instance from the check to allow updates.
        """
        if value:
            value = value.strip()  # Trim whitespace
            if not value:
                return None  # Treat it as None if value is empty after stripping whitespace
            
            # Prepare a query to check for existing passport numbers, excluding the current instance if updating
            query = Client.objects.filter(passport_number=value)
            if self.instance is not None:  # If this is an update operation
                query = query.exclude(pk=self.instance.pk)  # Exclude current instance from duplicate check

            if query.exists():
                raise serializers.ValidationError("This Passport Number is already in use.")
        else:
            return None  # Treat empty input as None
        return value
    
    def validate_national_id(self, value):
        """
        Check that the national ID is unique if provided and not empty, 
        excluding the current instance from the check to allow updates.
        """
        if value:
            value = value.strip()  # Trim whitespace
            if not value:
                return None  # Treat it as None if value is empty after stripping whitespace
            
            # Prepare a query to check for existing national IDs, excluding the current instance if updating
            query = Client.objects.filter(national_id=value)
            if self.instance is not None:  # If this is an update operation
                query = query.exclude(pk=self.instance.pk)  # Exclude current instance from duplicate check

            if query.exists():
                raise serializers.ValidationError("This national ID is already in use.")
        else:
            return None  # Treat empty input as None
        return value
    
    def validate(self, data):
        """
        Perform custom validation to ensure either national_id or passport_number is provided.
        If passport_number is provided, ensure passport_country is also provided.
        """
        national_id = data.get('national_id', None)
        passport_number = data.get('passport_number', None)
        passport_country = data.get('passport_country', None)

        # Check if both national_id and passport_number are missing or empty
        if (not national_id or national_id == "") and (not passport_number or passport_number == ""):
            raise serializers.ValidationError("Either National ID or Passport Number must be provided.")

        # If passport_number is provided (and not just an empty string), ensure passport_country is also provided
        if passport_number and not passport_country:
            raise serializers.ValidationError("Passport Country must be provided if Passport Number is specified.")

        # Ensuring at least one contact is provided        
        contacts = data.get('contacts', [])
        if not contacts:
            raise serializers.ValidationError("At least one contact must be provided.")
        
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['age'] = instance.get_age()
        return representation



