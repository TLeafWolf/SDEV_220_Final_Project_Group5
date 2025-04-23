# inventory/admin.py

from django.contrib import admin
from .models import Supply

class SupplyAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'location')  # Fields to display in the list view
    search_fields = ('name',)  # Add a search box for the name field
    ordering = ('name',)  # Default ordering by name

# Register the Supply model with the custom admin class
admin.site.register(Supply, SupplyAdmin)


