from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="E-mail")  # Torna o e-mail único e obrigatório
    is_active = models.BooleanField(default=True, verbose_name="Usuário ativo")  # Para desativar/excluir usuários

    def __str__(self):
        return self.username

class Arena(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome da Arena")
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")
    endereco = models.CharField(max_length=300, blank=True, null=True, verbose_name="Endereço")
    capacidade = models.IntegerField(blank=True, null=True, verbose_name="Capacidade")
    tipo_esporte = models.CharField(max_length=100, verbose_name="Tipo de Esporte")
    
    # Relacionamento com usuário que cadastrou
    usuario = models.ForeignKey(
        get_user_model(), 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='arenas_cadastradas'
    )
    
    data_cadastro = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True, verbose_name="Ativo")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Arena"
        verbose_name_plural = "Arenas"
        ordering = ['-data_cadastro']
