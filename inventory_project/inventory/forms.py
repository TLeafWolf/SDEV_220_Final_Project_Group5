
from django.core.validators import RegexValidator
from django import forms
from .models import Supply
from django.contrib.auth.models import User, Group

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


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserDeletionForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Select User to Delete")


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = User
        fields = ['username', 'group', 'password']
