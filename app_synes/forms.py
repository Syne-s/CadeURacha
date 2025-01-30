from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.validators import RegexValidator
from .models import Arena, Jogo

class ArenaForm(forms.ModelForm):
    class Meta:
        model = Arena
        fields = ['nome', 'endereco', 'latitude', 'longitude', 'logradouro', 'bairro', 'cidade', 'estado', 'regiao', 'cep', 'pais']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'foto_perfil']  # Add 'foto_perfil' field
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de Usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control'})  # Add widget for file input
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha Atual'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nova Senha'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a Nova Senha'}))

class JogoForm(forms.ModelForm):
    horario = forms.CharField(
        max_length=5,
        validators=[RegexValidator(regex=r'^\d{2}:\d{2}$', message="Formato de hora inválido, use HH:MM")],
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
            'required': True
        })
    )
    bolas = forms.IntegerField(
        widget=forms.HiddenInput(attrs={
            'id': 'qtd-bolas',  # Você pode manter o ID se precisar acessá-lo no front-end
        }),
        initial=0,
        required=True
    )

    class Meta:
        model = Jogo
        fields = ['titulo', 'descricao', 'data', 'horario', 'max_jogadores', 'arena','bolas']

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        horario = cleaned_data.get('horario')
        arena = cleaned_data.get('arena')

        if data and horario and arena:
            # Verificar se já existe um jogo com a mesma data, horário e arena
            conflito = Jogo.objects.filter(data=data, horario=horario, arena=arena).exists()
            if conflito:
                raise forms.ValidationError("Já existe um jogo marcado para esta data, horário e quadra.")
        return cleaned_data