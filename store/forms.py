# Import forms for Django forms
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re



# Formular pentru checkout (Shipping + Contact)
class CheckoutForm(forms.Form):
    full_name = forms.CharField(label='Nume complet', max_length=100)
    country = forms.CharField(label='Țara', max_length=50)
    region = forms.CharField(label='Regiune', max_length=50, required=False)
    city = forms.CharField(label='Oraș', max_length=50)
    zip_code = forms.CharField(label='Cod poștal', max_length=20)
    address = forms.CharField(label='Adresă', max_length=255)
    apartment = forms.CharField(label='Apartament', max_length=20, required=False)
    house_number = forms.CharField(label='Număr casă', max_length=20, required=False)
    phone = forms.CharField(label='Telefon', max_length=20)
    email = forms.EmailField(label='Email')


class ModernRegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Nume',
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Nume'})
    )
    last_name = forms.CharField(
        label='Prenume',
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Prenume'})
    )
    password1 = forms.CharField(
        label='Parolă',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Parolă'}),
        help_text='Minim 8 caractere, literă mare, cifră, simbol.'
    )
    password2 = forms.CharField(
        label='Confirmă Parola',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirmă Parola'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'})
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Acest email este deja folosit.')
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError('Parola trebuie să aibă minim 8 caractere.')
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Parola trebuie să conțină cel puțin o literă mare.')
        if not re.search(r'\d', password):
            raise ValidationError('Parola trebuie să conțină cel puțin o cifră.')
        if not re.search(r'[^\w\s]', password):
            raise ValidationError('Parola trebuie să conțină cel puțin un simbol.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Parolele nu coincid.')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
