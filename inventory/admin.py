from django.contrib import admin

# Register your models here.
# inventory/admin.py
from django.contrib import admin
from .models import InventoryItem

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'price', 'created_at', 'updated_at']
    search_fields = ['name']
