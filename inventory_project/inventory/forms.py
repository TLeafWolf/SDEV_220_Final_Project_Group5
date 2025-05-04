
from django.core.validators import RegexValidator
from django import forms
from .models import Supply

aisle_bay_validator = RegexValidator(
    regex=r'^[A-Z]/\d+$',
    message='Location must be in the format "A/12", where "A" is a letter and "12" is a number.',
    code='invalid_format'
)

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
        widgets = {
            'location': forms.TextInput(attrs={'placeholder': 'A/12'}),
        }

    def __init__(self, *args, **kwargs):
        super(SupplyForm, self).__init__(*args, **kwargs)
        self.fields['location'].validators.append(aisle_bay_validator) 

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a CSV file to upload')