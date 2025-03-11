import os
import requests
import tempfile
import cloudinary
import cloudinary.uploader
from django.core.management.base import BaseCommand
from django.conf import settings
from app_synes.models import Arena, Jogo

class Command(BaseCommand):
    help = 'Manually upload specific image files to Cloudinary'

    def add_arguments(self, parser):
        parser.add_argument('--path', required=True, help='Path to the local image file')
        parser.add_argument('--model', choices=['arena', 'jogo'], required=True, help='Model type (arena or jogo)')
        parser.add_argument('--id', required=True, type=int, help='ID of the model instance')

    def handle(self, *args, **options):
        path = options['path']
        model_type = options['model']
        instance_id = options['id']
        
        # Check if file exists
        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR(f"File not found: {path}"))
            return
            
        self.stdout.write(f"Processing {path} for {model_type} #{instance_id}")
        
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
            api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
            api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
            secure=True
        )
        
        try:
            # Get the instance
            if model_type == 'arena':
                instance = Arena.objects.get(id=instance_id)
                field_name = 'foto_quadra'
                folder = 'arenas'
            else:  # jogo
                instance = Jogo.objects.get(id=instance_id)
                field_name = 'imagem'
                folder = 'rachas'
                
            # Get the filename
            file_name = os.path.basename(path)
            
            # Upload to Cloudinary
            public_id = f"cadeURacha/{folder}/{os.path.splitext(file_name)[0]}"
            
            result = cloudinary.uploader.upload(
                path,
                public_id=public_id,
                overwrite=True,
                resource_type="image"
            )
            
            # Get the field
            field = getattr(instance, field_name)
            
            # Read file content
            with open(path, 'rb') as f:
                content = f.read()
                
            # Update the model field
            from django.core.files.base import ContentFile
            field.save(file_name, ContentFile(content), save=True)
            
            self.stdout.write(self.style.SUCCESS(f"Successfully uploaded to Cloudinary: {result['secure_url']}"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
