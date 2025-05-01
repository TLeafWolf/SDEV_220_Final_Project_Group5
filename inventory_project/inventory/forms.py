

from django import forms
from .models import Supply

class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ['name', 'price', 'quantity', 'location']

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a CSV file to upload')