import os
from django.core.management.base import BaseCommand
from django.db.models import Q
import cloudinary
import cloudinary.uploader
from app_synes.models import CustomUser, Arena, Jogo

class Command(BaseCommand):
    help = 'Fix image URLs in database to use Cloudinary'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database URL correction'))
        
        # Set up counters
        users_fixed = 0
        arenas_fixed = 0
        jogos_fixed = 0
        
        # Process user profile images
        self.stdout.write('Processing user profile images...')
        users = CustomUser.objects.filter(
            Q(foto_perfil__isnull=False) & 
            ~Q(foto_perfil='') & 
            ~Q(foto_perfil__contains='cloudinary') &
            ~Q(foto_perfil__contains='res.cloudinary.com')
        )
        
        for user in users:
            try:
                file_name = os.path.basename(user.foto_perfil.name)
                cloudinary_url = f"https://res.cloudinary.com/{os.environ.get('CLOUDINARY_CLOUD_NAME', 'dgzifammt')}/image/upload/v1/cadeURacha/perfil/{os.path.splitext(file_name)[0]}"
                user.foto_perfil.name = cloudinary_url
                user.save()
                users_fixed += 1
                self.stdout.write(f"   Fixed User #{user.pk} - {user.username}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   Error fixing User #{user.pk}: {str(e)}"))
        
        # Process arena images
        self.stdout.write('Processing arena images...')
        arenas = Arena.objects.filter(
            Q(foto_quadra__isnull=False) & 
            ~Q(foto_quadra='') & 
            ~Q(foto_quadra__contains='cloudinary') &
            ~Q(foto_quadra__contains='res.cloudinary.com')
        )
        
        for arena in arenas:
            try:
                file_name = os.path.basename(arena.foto_quadra.name)
                cloudinary_url = f"https://res.cloudinary.com/{os.environ.get('CLOUDINARY_CLOUD_NAME', 'dgzifammt')}/image/upload/v1/cadeURacha/arenas/{os.path.splitext(file_name)[0]}"
                arena.foto_quadra.name = cloudinary_url
                arena.save()
                arenas_fixed += 1
                self.stdout.write(f"   Fixed Arena #{arena.pk} - {arena.nome}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   Error fixing Arena #{arena.pk}: {str(e)}"))
        
        # Process jogo/racha images
        self.stdout.write('Processing jogo images...')
        jogos = Jogo.objects.filter(
            Q(imagem__isnull=False) & 
            ~Q(imagem='') & 
            ~Q(imagem__contains='cloudinary') &
            ~Q(imagem__contains='res.cloudinary.com')
        )
        
        for jogo in jogos:
            try:
                file_name = os.path.basename(jogo.imagem.name)
                cloudinary_url = f"https://res.cloudinary.com/{os.environ.get('CLOUDINARY_CLOUD_NAME', 'dgzifammt')}/image/upload/v1/cadeURacha/rachas/{os.path.splitext(file_name)[0]}"
                jogo.imagem.name = cloudinary_url
                jogo.save()
                jogos_fixed += 1
                self.stdout.write(f"   Fixed Jogo #{jogo.pk} - {jogo.titulo}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   Error fixing Jogo #{jogo.pk}: {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS(f'Fixed {users_fixed} user profile images'))
        self.stdout.write(self.style.SUCCESS(f'Fixed {arenas_fixed} arena images'))
        self.stdout.write(self.style.SUCCESS(f'Fixed {jogos_fixed} jogo images'))
        self.stdout.write(self.style.SUCCESS(f'Total fixed: {users_fixed + arenas_fixed + jogos_fixed} images'))
