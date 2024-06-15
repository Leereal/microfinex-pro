from rest_framework import generics
from .models import Client, Contact
from .serializers import ClientSerializer, ContactSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q

# Assuming ClientSerializer and ContactSerializer are defined appropriately

class AllClientsListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        This view should return a list of all clients
        for the currently authenticated user's active branch.
        """
        user = self.request.user
        return Client.objects.filter(branch=user.active_branch)
    
    def perform_create(self, serializer):
        ip_address = self.request.META.get('REMOTE_ADDR')
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        print("IP Address: ", ip_address)
        serializer.save(created_by=self.request.user, branch=self.request.user.active_branch, ip_address=ip_address, device_details=user_agent)

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        This view allows for retrieving, updating, or deleting a client
        based on the currently authenticated user's active branch.
        """
        user = self.request.user
        return Client.objects.filter(branch=user.active_branch)
    

class AllContactsListView(generics.ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ContactsListCreateView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        This view should return a list of all contacts
        associated with clients in the currently authenticated user's active branch.
        """
        user = self.request.user
        return Contact.objects.filter(client__branch=user.active_branch)

class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        This view allows for retrieving, updating, or deleting a client
        based on the currently authenticated user's active branch.
        """
        user = self.request.user
        return Contact.objects.filter(client__branch=user.active_branch)