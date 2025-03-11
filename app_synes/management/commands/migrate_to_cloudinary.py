import os
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.core.files import File
from django.conf import settings
import cloudinary.uploader
from app_synes.models import CustomUser, Arena, Jogo  # Import relevant models

class Command(BaseCommand):
    help = 'Migrates existing images to Cloudinary and updates database references'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting migration to Cloudinary'))
        
        # Process user profile images
        self.stdout.write('Migrating user profile images...')
        users = CustomUser.objects.exclude(foto_perfil='').exclude(foto_perfil__isnull=True)
        self.stdout.write(f'Found {users.count()} user profile images to migrate')
        
        for user in users:
            try:
                if user.foto_perfil and os.path.exists(user.foto_perfil.path):
                    self.stdout.write(f'Processing user profile image for {user.username}')
                    
                    # Upload the image to Cloudinary directly
                    result = cloudinary.uploader.upload(user.foto_perfil.path)
                    
                    # Open the file
                    with open(user.foto_perfil.path, 'rb') as f:
                        # Create a new Django File object
                        file_obj = File(f)
                        
                        # Save to the model field which will use Cloudinary storage
                        user.foto_perfil.save(
                            os.path.basename(user.foto_perfil.name),
                            file_obj,
                            save=True
                        )
                    
                    self.stdout.write(self.style.SUCCESS(f'Migrated profile image for {user.username}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing user {user.username}: {str(e)}'))
        
        # Process arena/quadra images
        self.stdout.write('Migrating arena/quadra images...')
        arenas = Arena.objects.exclude(foto_quadra='').exclude(foto_quadra__isnull=True)
        self.stdout.write(f'Found {arenas.count()} arena images to migrate')
        
        for arena in arenas:
            try:
                if arena.foto_quadra and os.path.exists(arena.foto_quadra.path):
                    self.stdout.write(f'Processing arena image for {arena.nome}')
                    
                    # Open the file
                    with open(arena.foto_quadra.path, 'rb') as f:
                        # Create a new Django File object
                        file_obj = File(f)
                        
                        # Save to the model field which will use Cloudinary storage
                        arena.foto_quadra.save(
                            os.path.basename(arena.foto_quadra.name),
                            file_obj,
                            save=True
                        )
                    
                    self.stdout.write(self.style.SUCCESS(f'Migrated arena image for {arena.nome}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing arena {arena.nome}: {str(e)}'))
        
        # Process racha/jogo images
        self.stdout.write('Migrating racha/jogo images...')
        jogos = Jogo.objects.exclude(imagem='').exclude(imagem__isnull=True)
        self.stdout.write(f'Found {jogos.count()} racha images to migrate')
        
        for jogo in jogos:
            try:
                if jogo.imagem and os.path.exists(jogo.imagem.path):
                    self.stdout.write(f'Processing racha image for {jogo.titulo}')
                    
                    # Open the file
                    with open(jogo.imagem.path, 'rb') as f:
                        # Create a new Django File object
                        file_obj = File(f)
                        
                        # Save to the model field which will use Cloudinary storage
                        jogo.imagem.save(
                            os.path.basename(jogo.imagem.name),
                            file_obj,
                            save=True
                        )
                    
                    self.stdout.write(self.style.SUCCESS(f'Migrated racha image for {jogo.titulo}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing racha {jogo.titulo}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully migrated all images to Cloudinary'))
