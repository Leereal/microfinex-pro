from django.urls import path
from .views import AllClientsListView, AllContactsListView, ClientDetailView, ClientListCreateView, ContactDetailView, ContactsListCreateView
urlpatterns = [
    # Paths for Client operations
    path('clients/all', AllClientsListView.as_view(), name='client-list'),
    path('clients/', ClientListCreateView.as_view(), name='client-list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),

    # Paths for Contact operations
    path('contacts/all', AllContactsListView.as_view(), name='contact-list-create'),
    path('contacts/', ContactsListCreateView.as_view(), name='contact-list-create'),
    path('contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),
]
