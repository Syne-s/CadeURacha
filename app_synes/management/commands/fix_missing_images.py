from django.core.management.base import BaseCommand
from app_synes.models import Arena, Jogo

class Command(BaseCommand):
    help = 'Ensure all arenas and jogos have image URLs set correctly'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Checking for arenas and jogos without images...'))
        
        # Import default image URLs
        try:
            from app_synes.default_images import DEFAULT_QUADRA_IMAGE_URL, DEFAULT_RACHA_IMAGE_URL
            
            # Fix arenas without images
            arenas_without_images = Arena.objects.filter(foto_quadra__isnull=True, foto_url__isnull=True)
            self.stdout.write(f"Found {arenas_without_images.count()} arenas without images")
            
            for arena in arenas_without_images:
                arena.foto_url = DEFAULT_QUADRA_IMAGE_URL
                arena.save()
                self.stdout.write(f"   Set default image for arena: {arena.nome}")
            
            # Fix jogos without images
            jogos_without_images = Jogo.objects.filter(imagem__isnull=True, foto_url__isnull=True)
            self.stdout.write(f"Found {jogos_without_images.count()} jogos without images")
            
            for jogo in jogos_without_images:
                jogo.foto_url = DEFAULT_RACHA_IMAGE_URL
                jogo.save()
                self.stdout.write(f"   Set default image for jogo: {jogo.titulo}")
            
            self.stdout.write(self.style.SUCCESS(f'Done! Fixed {arenas_without_images.count()} arenas and {jogos_without_images.count()} jogos'))
            
        except ImportError as e:
            self.stdout.write(self.style.ERROR(f'Error importing default image URLs: {e}'))
            self.stdout.write(self.style.ERROR('Make sure to run upload_default_images first'))
