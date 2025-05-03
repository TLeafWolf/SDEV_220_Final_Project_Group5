

from django import forms
from .models import Supply

class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ['name', 'price', 'quantity', 'location']
        labels = {
            'name': 'Name',
            'price': 'Price($)',
            'quantity': 'Quantity',
            'location': 'Aisle/Bay',
        }

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a CSV file to upload')