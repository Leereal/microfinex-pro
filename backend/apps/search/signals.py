from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry

from apps.clients.models import Client


@receiver(post_save, sender=Client)
def update_document(sender, instance=None, created=False, **kwargs):
    """Update the ClientDocument in Elasticsearch when an client instance is updated or created"""
    registry.update(instance)


@receiver(post_delete, sender=Client)
def delete_document(sender, instance=None, **kwargs):
    """Delete the ClientDocument in Elasticsearch when an client instance is deleted"""
    registry.delete(instance)