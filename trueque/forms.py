from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUsers, Comic, Offer
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
            'username': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'required': True}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'phonenumber': forms.TextInput(attrs={'class': 'form-control','required': True}),
            'municipality': forms.TextInput(attrs={'class': 'form-control','required': True}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
class ComicForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'  # Solo archivos de imagen
        }),
        required=True
    )

    class Meta:
        model = Comic
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['description', 'offered_item']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'offered_item': forms.TextInput(attrs={'class': 'form-control'}),
        }