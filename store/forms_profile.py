from django import forms
from .models import ShippingAddress

class ProfileForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'full_name', 'country', 'region', 'city', 'zip_code',
            'address', 'apartment', 'house_number', 'phone', 'email'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Nume complet'}),
            'country': forms.TextInput(attrs={'placeholder': 'Țara'}),
            'region': forms.TextInput(attrs={'placeholder': 'Regiune'}),
            'city': forms.TextInput(attrs={'placeholder': 'Oraș'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Cod poștal'}),
            'address': forms.Textarea(attrs={'placeholder': 'Adresă', 'rows': 2}),
            'apartment': forms.TextInput(attrs={'placeholder': 'Apartament'}),
            'house_number': forms.TextInput(attrs={'placeholder': 'Număr casă'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Telefon'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'})
        }
