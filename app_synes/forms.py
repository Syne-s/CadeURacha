import datetime
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.validators import RegexValidator
from .models import Arena, Jogo
from io import BytesIO
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
import re

class ArenaForm(forms.ModelForm):
    class Meta:
        model = Arena
        fields = ['nome', 'logradouro', 'bairro', 'cidade', 'estado',
                 'cep', 'latitude', 'longitude', 'foto_quadra']

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Construir o endereço completo
        endereco_parts = []
        if self.cleaned_data.get('logradouro'): 
            endereco_parts.append(self.cleaned_data['logradouro'])
        if self.cleaned_data.get('bairro'):
            endereco_parts.append(self.cleaned_data['bairro'])
        if self.cleaned_data.get('cidade'):
            endereco_parts.append(self.cleaned_data['cidade'])
        if self.cleaned_data.get('estado'):
            endereco_parts.append(self.cleaned_data['estado'])
        if self.cleaned_data.get('cep'):
            endereco_parts.append(self.cleaned_data['cep'])
        
        # Atualizar o campo endereço
        instance.endereco = ', '.join(filter(None, endereco_parts))
        
        if commit:
            instance.save()
        return instance

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'foto_perfil']  # Add 'foto_perfil' field
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de Usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control'})  # Add widget for file input
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('foto_perfil'):
            image = Image.open(self.cleaned_data['foto_perfil'])
            image = self._process_image(image)
            image_io = BytesIO()
            image.save(image_io, format='JPEG')
            instance.foto_perfil.save(self.cleaned_data['foto_perfil'].name, ContentFile(image_io.getvalue()), save=False)
        if commit:
            instance.save()
        return instance

    def _process_image(self, image):
        # Define the desired size
        desired_size = (300, 300)  # Adjust as needed
        image = ImageOps.fit(image, desired_size, Image.Resampling.LANCZOS, centering=(0.5, 0.5))
        return image

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha Atual'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nova Senha'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a Nova Senha'}))

class JogoForm(forms.ModelForm):
    arena = forms.ModelChoiceField(
        queryset=Arena.objects.all(),
        empty_label="Selecione uma quadra",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Jogo
        fields = ['titulo', 'descricao', 'arena', 'data', 'horario', 'bolas', 'imagem']  # Removido max_jogadores
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
            'bolas': forms.HiddenInput(attrs={'id': 'qtd-bolas'})
        }

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        horario = cleaned_data.get('horario')
        arena = cleaned_data.get('arena')

        if data and horario and arena:
            # Convert horario to a time object if it's a string
            if isinstance(horario, str):
                try:
                    horario_obj = datetime.datetime.strptime(horario, "%H:%M").time()
                except ValueError:
                    raise forms.ValidationError("Formato de hora inválido, use HH:MM.")
            else:
                horario_obj = horario

            new_start = datetime.datetime.combine(data, horario_obj)
            new_end = new_start + datetime.timedelta(hours=2)

            # Buscar jogos na mesma quadra e data
            conflitos = Jogo.objects.filter(data=data, arena=arena)
            for jogo in conflitos:
                existing_start = datetime.datetime.combine(
                    jogo.data,
                    datetime.datetime.strptime(jogo.horario, "%H:%M").time()
                )
                existing_end = existing_start + datetime.timedelta(hours=2)
                if new_start < existing_end and new_end > existing_start:
                    raise forms.ValidationError(
                        f"Já existe um jogo marcado na quadra '{arena.nome}' no horário selecionado ({horario_obj.strftime('%H:%M')})."
                    )
        return cleaned_data

class CustomUserForm(forms.ModelForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        pattern = re.compile(r'^[a-zA-Z](?!.*__)[a-zA-Z0-9]*(_[a-zA-Z0-9]+)*$')
        
        if len(username) < 4 or len(username) > 20:
            raise forms.ValidationError(
                "O nome de usuário deve ter entre 4 e 20 caracteres."
            )
            
        if not pattern.match(username):
            raise forms.ValidationError(
                "Nome de usuário inválido. Deve começar com uma letra, pode conter letras, "
                "números e sublinhados (não consecutivos e não no início/fim)."
            )
            
        return username