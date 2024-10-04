# inventory/serializers.py
from rest_framework import serializers
from .models import InventoryItem

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ['id', 'name', 'description', 'quantity', 'price', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        """
        Check that the name field is not empty.
        """
        if not value.strip():  # Check if name is empty or contains only whitespace
            raise serializers.ValidationError("The name field cannot be empty.")
        return value
