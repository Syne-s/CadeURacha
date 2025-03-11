import os
from django.core.management.base import BaseCommand
from app_synes.models import CustomUser, Arena, Jogo
import re

class Command(BaseCommand):
    help = 'Fix existing Cloudinary URLs in database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Cloudinary URL fixes'))
        
        # Fix user profile images
        users_fixed = 0
        
        # Caso 1: URL do Cloudinary no campo foto_perfil
        for user in CustomUser.objects.filter(foto_perfil__isnull=False):
            try:
                # Verifica se o campo foto_perfil contém uma URL do Cloudinary
                if hasattr(user.foto_perfil, 'url') and 'res.cloudinary.com' in user.foto_perfil.url:
                    user.foto_url = user.foto_perfil.url
                    # Não limpar foto_perfil aqui, apenas definir a URL correta
                    user.save()
                    users_fixed += 1
                    self.stdout.write(f"Fixed URL for user {user.username}: {user.foto_url}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing user {user.username}: {str(e)}"))
                
        # Caso 2: String URL incorreta no campo foto_perfil (deve ir para foto_url)
        cloudinary_pattern = re.compile(r'https?://res\.cloudinary\.com/')
        for user in CustomUser.objects.all():
            try:
                if isinstance(user.foto_perfil, str) and cloudinary_pattern.search(user.foto_perfil):
                    self.stdout.write(f"Found Cloudinary URL string in foto_perfil for {user.username}")
                    user.foto_url = user.foto_perfil
                    user.foto_perfil = None  # Limpar o campo incorreto
                    user.save()
                    users_fixed += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fixing URL string for user {user.username}: {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS(f'Fixed {users_fixed} Cloudinary URLs'))
