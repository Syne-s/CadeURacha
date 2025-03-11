import os
import tempfile
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import requests
import cloudinary
import cloudinary.uploader
from django.conf import settings
from app_synes.models import CustomUser, Arena, Jogo

class Command(BaseCommand):
    help = 'Upload specific images to Cloudinary and update database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--download-base-url',
            default='http://localhost:8000',
            help='Base URL to download images from'
        )

    def handle(self, *args, **options):
        base_url = options['download_base_url']
        self.stdout.write(self.style.SUCCESS(f'Starting Cloudinary upload with base URL: {base_url}'))
        
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
            api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
            api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
            secure=True
        )
        
        # Process arenas
        self.stdout.write('Processing arenas...')
        arenas = Arena.objects.filter(foto_quadra__isnull=False).exclude(foto_quadra='')
        for arena in arenas:
            try:
                # Format source URL
                src_url = arena.foto_quadra.url
                if src_url.startswith('/'):
                    src_url = f"{base_url}{src_url}"
                
                # Download image
                self.stdout.write(f"   Downloading from {src_url}")
                response = requests.get(src_url, stream=True)
                if response.status_code != 200:
                    self.stdout.write(self.style.ERROR(f"   Failed to download: {response.status_code}"))
                    continue
                
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False) as temp:
                    temp.write(response.content)
                    temp_path = temp.name
                
                # Upload to Cloudinary
                file_name = os.path.basename(arena.foto_quadra.name)
                public_id = f"cadeURacha/arenas/{os.path.splitext(file_name)[0]}"
                result = cloudinary.uploader.upload(
                    temp_path,
                    public_id=public_id,
                    overwrite=True,
                    resource_type="image"
                )
                
                # Clean up temp file
                os.unlink(temp_path)
                
                # Update model
                arena.foto_quadra.name = result['secure_url']
                arena.save()
                
                self.stdout.write(self.style.SUCCESS(f"   Uploaded arena image for {arena.nome}: {result['secure_url']}"))
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   Error processing arena {arena.nome}: {str(e)}"))
        
        # Process jogos
        self.stdout.write('Processing jogos...')
        jogos = Jogo.objects.filter(imagem__isnull=False).exclude(imagem='')
        for jogo in jogos:
            try:
                # Format source URL
                src_url = jogo.imagem.url
                if src_url.startswith('/'):
                    src_url = f"{base_url}{src_url}"
                
                # Download image
                self.stdout.write(f"   Downloading from {src_url}")
                response = requests.get(src_url, stream=True)
                if response.status_code != 200:
                    self.stdout.write(self.style.ERROR(f"   Failed to download: {response.status_code}"))
                    continue
                
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False) as temp:
                    temp.write(response.content)
                    temp_path = temp.name
                
                # Upload to Cloudinary
                file_name = os.path.basename(jogo.imagem.name)
                public_id = f"cadeURacha/rachas/{os.path.splitext(file_name)[0]}"
                result = cloudinary.uploader.upload(
                    temp_path,
                    public_id=public_id,
                    overwrite=True,
                    resource_type="image"
                )
                
                # Clean up temp file
                os.unlink(temp_path)
                
                # Update model
                jogo.imagem.name = result['secure_url']
                jogo.save()
                
                self.stdout.write(self.style.SUCCESS(f"   Uploaded jogo image for {jogo.titulo}: {result['secure_url']}"))
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   Error processing jogo {jogo.titulo}: {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS('Upload to Cloudinary completed'))
