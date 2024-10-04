

# Create your models here.
# inventory/models.py
from django.db import models
from django.contrib.auth.models import User

class InventoryItem(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Unique name for the item
    description = models.TextField() 
    quantity = models.IntegerField()  
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the item
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the item was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the item was last updated
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
