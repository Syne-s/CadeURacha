from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Arena

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail")
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class ArenaForm(forms.ModelForm):
    class Meta:
        model = Arena
        fields = ['nome', 'latitude', 'longitude', 'endereco', 'capacidade', 'tipo_esporte']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }