import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
import requests
import tempfile
from urllib.parse import urlparse
import cloudinary
import cloudinary.uploader
from app_synes.models import CustomUser, Arena, Jogo

class Command(BaseCommand):
    help = 'Alternative approach to migrate existing images to Cloudinary'

    def handle_model_images(self, model_name, queryset, field_name):
        self.stdout.write(f'Processing {model_name} images...')
        count = 0
        
        for item in queryset:
            try:
                # Get the field value
                field = getattr(item, field_name)
                if not field:
                    continue
                
                # Get the file name without path
                file_name = os.path.basename(field.name)
                
                # Skip if already on Cloudinary
                if 'cloudinary' in field.url.lower() or 'res.cloudinary.com' in field.url.lower():
                    self.stdout.write(f"   Already on Cloudinary: {field.url}")
                    continue
                
                self.stdout.write(f"   Processing {model_name} #{getattr(item, 'pk', 'unknown')} - {file_name}")
                
                file_content = None
                
                # Try to get the local file path first
                try:
                    if hasattr(field, 'path') and field.path and os.path.exists(field.path):
                        with open(field.path, 'rb') as f:
                            file_content = f.read()
                            self.stdout.write(f"   Found local file: {field.path}")
                except Exception as e:
                    self.stdout.write(f"   Error accessing local file: {str(e)}")
                
                # If local file doesn't work, try to download from URL
                if file_content is None:
                    try:
                        # Handle relative URLs by adding base URL
                        url = field.url
                        if url.startswith('/'):
                            # Get the base URL from settings if available, otherwise use localhost
                            base_url = os.environ.get('BASE_URL', 'http://localhost:8000')
                            url = f"{base_url}{url}"
                        
                        self.stdout.write(f"   Trying to download from URL: {url}")
                        response = requests.get(url, stream=True)
                        if response.status_code == 200:
                            file_content = response.content
                            self.stdout.write(f"   Successfully downloaded from URL")
                        else:
                            self.stdout.write(self.style.WARNING(f"   Cannot download from URL: {url}, status: {response.status_code}"))
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"   Error downloading file: {str(e)}"))
                
                # If we couldn't get file content, create a placeholder
                if file_content is None:
                    self.stdout.write(self.style.WARNING(f"   Creating placeholder for {field.name}"))
                    
                    # For testing purposes, try to use a default image
                    placeholder_path = os.path.join(settings.BASE_DIR, 'app_synes', 'static', 'app_synes', 'images', 'user-default.jpg')
                    if os.path.exists(placeholder_path):
                        with open(placeholder_path, 'rb') as f:
                            file_content = f.read()
                            self.stdout.write(f"   Using placeholder image")
                    else:
                        self.stdout.write(self.style.ERROR(f"   Cannot find placeholder image"))
                        continue
                
                # Upload to Cloudinary directly
                try:
                    # Write to temp file for Cloudinary upload
                    with tempfile.NamedTemporaryFile(delete=False) as temp:
                        temp.write(file_content)
                        temp.flush()
                        temp_path = temp.name
                    
                    # Upload to Cloudinary
                    category = 'perfil' if model_name == 'User' else ('arenas' if model_name == 'Arena' else 'rachas')
                    public_id = f"cadeURacha/{category}/{os.path.splitext(file_name)[0]}"
                    
                    result = cloudinary.uploader.upload(
                        temp_path,
                        public_id=public_id,
                        overwrite=True,
                        resource_type="image"
                    )
                    
                    os.unlink(temp_path)  # Delete the temp file
                    
                    # Create a ContentFile and save to the model field
                    content_file = ContentFile(file_content)
                    
                    # Use the secure URL from Cloudinary
                    cloudinary_url = result['secure_url']
                    
                    # Get the original name part for saving
                    original_name = os.path.basename(field.name)
                    
                    # Update the field with new file
                    getattr(item, field_name).save(
                        name=original_name,  # Keep original filename
                        content=content_file,
                        save=False
                    )
                    
                    # Make sure the URL is correctly set
                    setattr(item, f"{field_name}_url", cloudinary_url)
                    
                    # Save the model instance
                    item.save()
                    
                    self.stdout.write(self.style.SUCCESS(f"   Successfully uploaded to Cloudinary: {cloudinary_url}"))
                    count += 1
                    
                except Exception as upload_error:
                    self.stdout.write(self.style.ERROR(f"   Cloudinary upload error: {str(upload_error)}"))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   Error processing {model_name} #{getattr(item, 'pk', 'unknown')}: {str(e)}"))
                
        return count

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting alternative migration to Cloudinary'))
        
        # Verify Cloudinary config
        if not all([settings.CLOUDINARY_STORAGE.get('CLOUD_NAME'), 
                   settings.CLOUDINARY_STORAGE.get('API_KEY'),
                   settings.CLOUDINARY_STORAGE.get('API_SECRET')]):
            self.stdout.write(self.style.ERROR('Cloudinary settings are missing or incomplete'))
            return
            
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
            api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
            api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
            secure=True
        )
        
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
