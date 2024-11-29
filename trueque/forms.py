from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUsers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': True})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and not CustomUsers.objects.filter(username=username).exists():
            raise forms.ValidationError(_('El usuario no existe.'))

        user = authenticate(username=username, password=password)
        if username and password and user is None:
            raise forms.ValidationError(_('La contraseña es incorrecta.'))

        return cleaned_data

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUsers
        fields = ('first_name', 'username', 'phonenumber',  'email', 'password', 'state', 'municipality')
        labels = {
            'first_name': 'Nombre',
            'username': 'Usuario',
            'email': 'Correo',
            'password': 'Contraseña',
            'state': 'Estado',
            'phonenumber': 'Telefono',
            'municipality': 'Municipio'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'username': forms.TextInput(attrs={'class': 'form-control',}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'password': forms.PasswordInput(attrs={'class': 'form-control',}),
            'state': forms.TextInput(attrs={'class': 'form-control',}),
            'phonenumber': forms.TextInput(attrs={'class': 'form-control',}),
            'municipality': forms.TextInput(attrs={'class': 'form-control',}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user