# inventory/forms.py

from django import forms
from .models import Supply

class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ['name', 'price', 'quantity', 'location']
