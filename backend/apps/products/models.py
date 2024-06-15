from django.db import models
from apps.common.models import TimeStampedModel

class Product(TimeStampedModel):
    """
    Product model represents a product with a name and an active status.
    Inherits timestamps from TimeStampedModel for created_at and last_modified fields.
    """
    name = models.CharField(max_length=255, help_text="The name of the product.")
    is_active = models.BooleanField(default=True, help_text="Indicates whether the product is active.")

    def __str__(self):
        """
        String representation of the Product model.
        Returns the name of the product.
        """
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["name"]  # Orders products alphabetically by name
