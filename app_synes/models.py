from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="E-mail")  # Torna o e-mail único e obrigatório
    is_active = models.BooleanField(default=True, verbose_name="Usuário ativo")  # Para desativar/excluir usuários

    def __str__(self):
        return self.username
