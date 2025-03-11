from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="E-mail")
    is_active = models.BooleanField(default=True, verbose_name="Usuário ativo")
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)
    levar_bola = models.BooleanField(default=False, verbose_name="Levar bola")
    foto_url = models.URLField(blank=True, null=True, verbose_name="URL da foto")  # Campo para armazenar a URL completa

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        # Se foto_perfil for uma string e parece uma URL do Cloudinary, salvá-la em foto_url
        if isinstance(self.foto_perfil, str) and ('cloudinary' in self.foto_perfil.lower() or 'res.cloudinary.com' in self.foto_perfil.lower()):
            self.foto_url = self.foto_perfil
            # Limpar o campo foto_perfil para evitar confusão
            self.foto_perfil = None
        super().save(*args, **kwargs)
    
    @property
    def get_profile_image_url(self):
        """Retorna a URL correta da imagem de perfil"""
        # Primeiro verifica se há uma URL Cloudinary direta
        if self.foto_url:
            return self.foto_url
        # Se não, tenta o campo normal foto_perfil
        elif self.foto_perfil:
            return self.foto_perfil.url
        # Caso contrário, retorna a imagem padrão
        try:
            from app_synes.default_images import DEFAULT_PERFIL_IMAGE_URL
            return DEFAULT_PERFIL_IMAGE_URL or None
        except (ImportError, AttributeError):
            return None

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

class Arena(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome da Arena")
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")
    endereco = models.CharField(max_length=300, verbose_name="Endereço")
    
    # Campos para armazenar partes separadas do endereço
    logradouro = models.CharField(max_length=255, blank=True, null=True, verbose_name="Logradouro")
    bairro = models.CharField(max_length=255, blank=True, null=True, verbose_name="Bairro")
    cidade = models.CharField(max_length=255, blank=True, null=True, verbose_name="Cidade")
    estado = models.CharField(max_length=255, blank=True, null=True, verbose_name="Estado")
    regiao = models.CharField(max_length=255, blank=True, null=True, verbose_name="Região")
    cep = models.CharField(max_length=20, blank=True, null=True, verbose_name="CEP")
    pais = models.CharField(max_length=255, blank=True, null=True, verbose_name="País")
    
    foto_quadra = models.ImageField(upload_to='arenas/', null=True, blank=True)
    foto_url = models.URLField(blank=True, null=True, verbose_name="URL da foto da quadra")
    
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
    
    def save(self, *args, **kwargs):
        # Se foto_quadra for uma string e parece uma URL do Cloudinary, salvá-la em foto_url
        if isinstance(self.foto_quadra, str) and ('cloudinary' in self.foto_quadra.lower() or 'res.cloudinary.com' in self.foto_quadra.lower()):
            self.foto_url = self.foto_quadra
            # Limpar o campo foto_quadra para evitar confusão
            self.foto_quadra = None
        super().save(*args, **kwargs)
    
    @property
    def get_arena_image_url(self):
        """Retorna a URL correta da imagem da quadra"""
        # Primeiro verifica se há uma URL Cloudinary direta
        if self.foto_url:
            return self.foto_url
        # Se não, tenta o campo normal foto_quadra
        elif self.foto_quadra:
            return self.foto_quadra.url
        # Caso contrário, retorna a imagem padrão
        try:
            from app_synes.default_images import DEFAULT_QUADRA_IMAGE_URL
            return DEFAULT_QUADRA_IMAGE_URL or None
        except (ImportError, AttributeError):
            return None

    class Meta:
        verbose_name = "Quadra"
        verbose_name_plural = "Quadras"
        ordering = ['-data_cadastro']
        permissions = [
            ("can_add_arena", "Can add new arena on map")
        ]

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
    foto_url = models.URLField(blank=True, null=True, verbose_name="URL da foto do racha")
    
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        # Se imagem for uma string e parece uma URL do Cloudinary, salvá-la em foto_url
        if isinstance(self.imagem, str) and ('cloudinary' in self.imagem.lower() or 'res.cloudinary.com' in self.imagem.lower()):
            self.foto_url = self.imagem
            # Limpar o campo imagem para evitar confusão
            self.imagem = None
        super().save(*args, **kwargs)

    @property
    def get_jogo_image_url(self):
        """Retorna a URL correta da imagem do jogo"""
        # Primeiro verifica se há uma URL Cloudinary direta
        if self.foto_url:
            return self.foto_url
        # Se não, tenta o campo normal imagem
        elif self.imagem:
            return self.imagem.url
        # Caso contrário, retorna a imagem padrão
        try:
            from app_synes.default_images import DEFAULT_RACHA_IMAGE_URL
            return DEFAULT_RACHA_IMAGE_URL or None
        except (ImportError, AttributeError):
            return None
    
    class Meta:
        verbose_name = 'Racha'
        verbose_name_plural = 'Rachas'