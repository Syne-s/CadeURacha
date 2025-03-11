import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
import requests
import tempfile
from urllib.parse import urlparse
from app_synes.models import CustomUser, Arena, Jogo  # Import relevant models

class Command(BaseCommand):
    help = 'Alternative approach to migrate existing images to Cloudinary'

    def handle_model_images(self, model_name, queryset, field_name):
        self.stdout.write(f'Processing {model_name} images...')
        count = 0
        
        for item in queryset:
            field = getattr(item, field_name)
            if not field:
                continue
                
            try:
                # Get the file name without path
                file_name = os.path.basename(field.name)
                
                # Handle different storage scenarios
                if hasattr(field, 'url') and field.url:
                    # Try to get the path
                    try:
                        file_path = field.path
                        if os.path.exists(file_path):
                            with open(file_path, 'rb') as f:
                                # Save the file through Django's storage which will use Cloudinary
                                new_name = f"{model_name.lower()}_{item.pk}_{file_name}"
                                field.save(new_name, ContentFile(f.read()), save=False)
                                item.save()
                                count += 1
                                self.stdout.write(f"   Migrated {model_name} #{item.pk} - {new_name}")
                        else:
                            self.stdout.write(self.style.WARNING(f"   File doesn't exist at {file_path}"))
                    except (AttributeError, ValueError, FileNotFoundError) as e:
                        # Try to download from URL if path doesn't work
                        try:
                            parsed_url = urlparse(field.url)
                            if parsed_url.netloc and not parsed_url.netloc.endswith('cloudinary.com'):
                                response = requests.get(field.url, stream=True)
                                if response.status_code == 200:
                                    with tempfile.NamedTemporaryFile() as temp:
                                        for chunk in response.iter_content(chunk_size=1024):
                                            temp.write(chunk)
                                        temp.flush()
                                        new_name = f"{model_name.lower()}_{item.pk}_{file_name}"
                                        field.save(new_name, ContentFile(open(temp.name, 'rb').read()), save=False)
                                        item.save()
                                        count += 1
                                        self.stdout.write(f"   Downloaded and migrated {model_name} #{item.pk} - {new_name}")
                        except Exception as download_err:
                            self.stdout.write(self.style.WARNING(f"   Could not download from URL: {str(download_err)}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   Error processing {model_name} #{item.pk}: {str(e)}"))
                
        return count

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting alternative migration to Cloudinary'))
        
        # Process user profile images
        users = CustomUser.objects.filter(foto_perfil__isnull=False).exclude(foto_perfil='')
        user_count = self.handle_model_images('User', users, 'foto_perfil')
        self.stdout.write(self.style.SUCCESS(f'Migrated {user_count} user profile images'))
        
        # Process arena images
        arenas = Arena.objects.filter(foto_quadra__isnull=False).exclude(foto_quadra='')
        arena_count = self.handle_model_images('Arena', arenas, 'foto_quadra')
        self.stdout.write(self.style.SUCCESS(f'Migrated {arena_count} arena images'))
        
        # Process racha/jogo images
        jogos = Jogo.objects.filter(imagem__isnull=False).exclude(imagem='')
        jogo_count = self.handle_model_images('Jogo', jogos, 'imagem')
        self.stdout.write(self.style.SUCCESS(f'Migrated {jogo_count} racha images'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully completed migration with {user_count + arena_count + jogo_count} total images'))
