import os
import cloudinary
import cloudinary.uploader
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Upload default images to Cloudinary and save their URLs'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting upload of default images to Cloudinary'))
        
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
            api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
            api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
            secure=True
        )
        
        # Paths to default images
        base_path = os.path.join(settings.BASE_DIR, 'staticfiles', 'app_synes', 'images')
        default_images = {
            'racha': os.path.join(base_path, 'space.jpg'),
            'quadra': os.path.join(base_path, 'quadra.jpeg'),
            'perfil': os.path.join(base_path, 'user-default.jpg')
        }
        
        # Upload each image and save the URL
        results = {}
        for image_type, path in default_images.items():
            if not os.path.exists(path):
                self.stdout.write(self.style.ERROR(f"Default image not found: {path}"))
                continue
                
            try:
                self.stdout.write(f"Uploading {image_type} default image...")
                result = cloudinary.uploader.upload(
                    path,
                    public_id=f"cadeURacha/defaults/{image_type}_default",
                    overwrite=True
                )
                
                results[image_type] = result['secure_url']
                self.stdout.write(self.style.SUCCESS(f"Uploaded {image_type} default image: {result['secure_url']}"))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error uploading {image_type} default image: {str(e)}"))
        
        # Save URLs to settings file
        try:
            with open(os.path.join(settings.BASE_DIR, 'app_synes', 'default_images.py'), 'w') as f:
                f.write("# Default image URLs from Cloudinary\n\n")
                f.write(f"DEFAULT_RACHA_IMAGE_URL = '{results.get('racha', '')}'\n")
                f.write(f"DEFAULT_QUADRA_IMAGE_URL = '{results.get('quadra', '')}'\n")
                f.write(f"DEFAULT_PERFIL_IMAGE_URL = '{results.get('perfil', '')}'\n")
            
            self.stdout.write(self.style.SUCCESS('Default image URLs saved to default_images.py'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error saving URLs to file: {str(e)}"))
