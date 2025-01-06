from django import forms
from django.contrib.auth import get_user_model
from .models import Arena

class ArenaForm(forms.ModelForm):
    class Meta:
        model = Arena
        fields = ['nome', 'endereco', 'latitude', 'longitude', 'logradouro', 'bairro', 'cidade', 'estado', 'regiao', 'cep', 'pais']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de Usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
        }