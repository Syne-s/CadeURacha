from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="E-mail")
    is_active = models.BooleanField(default=True, verbose_name="Usuário ativo")
    foto_perfil = models.ImageField(upload_to='perfil/', null=True, blank=True, verbose_name="Foto de Perfil")
    levar_bola = models.BooleanField(default=False, verbose_name="Levar bola")

    def __str__(self):
        return self.username

class Arena(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome da Arena")
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")
    endereco = models.CharField(max_length=300, verbose_name="Endereço")
    capacidade = models.IntegerField(blank=True, null=True, verbose_name="Capacidade")
    tipo_esporte = models.CharField(max_length=100, verbose_name="Tipo de Esporte")
    
    # Campos para armazenar partes separadas do endereço
    logradouro = models.CharField(max_length=255, blank=True, null=True, verbose_name="Logradouro")
    bairro = models.CharField(max_length=255, blank=True, null=True, verbose_name="Bairro")
    cidade = models.CharField(max_length=255, blank=True, null=True, verbose_name="Cidade")
    estado = models.CharField(max_length=255, blank=True, null=True, verbose_name="Estado")
    regiao = models.CharField(max_length=255, blank=True, null=True, verbose_name="Região")
    cep = models.CharField(max_length=20, blank=True, null=True, verbose_name="CEP")
    pais = models.CharField(max_length=255, blank=True, null=True, verbose_name="País")
    
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

class Jogo(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data = models.DateField()
    horario = models.CharField(max_length=5, null=False, blank=False)  # Alterado para CharField
    max_jogadores = models.IntegerField(default=2000, verbose_name="Quantidade máxima de jogadores")  # Define um valor padrão
    arena = models.ForeignKey(Arena, on_delete=models.CASCADE, related_name='jogos')
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='jogos_cadastrados')
    participantes = models.ManyToManyField(CustomUser, related_name="jogos_participando",blank=True)
    criador_jogo = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='jogos_criados')
    bolas = models.IntegerField(default=0,verbose_name="Quantidade de bolas de basquete disponíveis")
    jogadores = models.ManyToManyField('CustomUser', related_name='jogos', blank=True)
    imagem = models.ImageField(
        upload_to='rachas/', 
        null=True, 
        blank=True, 
        verbose_name="Imagem do Racha"
    )
    
    def __str__(self):
        return self.titulo