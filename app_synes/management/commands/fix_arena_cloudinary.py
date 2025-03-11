import os
from django.core.management.base import BaseCommand
import re
from app_synes.models import Arena
import cloudinary
import cloudinary.uploader
from django.conf import settings
import tempfile
import requests
from django.db import connection

class Command(BaseCommand):
    help = 'Fix arena images URLs for Cloudinary'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Arena image fixes for Cloudinary'))
        
        # First, check if foto_url field exists
        has_foto_url = self._check_field_exists('app_synes_arena', 'foto_url')
        
        if not has_foto_url:
            self.stdout.write(self.style.WARNING('The foto_url field does not exist in Arena model. Please run migrations first.'))
            return
        
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
            api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
            api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
            secure=True
        )
        
        # Count of fixed arenas
        fixed = 0
        
        # Caso 1: Arenas com foto_quadra mas sem foto_url
        arenas = Arena.objects.filter(foto_quadra__isnull=False).exclude(foto_quadra='').filter(foto_url__isnull=True)
        self.stdout.write(f"Found {arenas.count()} arenas with foto_quadra but no foto_url")
        
        for arena in arenas:
            try:
                # Verificar se a URL já é do Cloudinary 
                if hasattr(arena.foto_quadra, 'url') and 'res.cloudinary.com' in arena.foto_quadra.url:
                    arena.foto_url = arena.foto_quadra.url
                    arena.save()
                    fixed += 1
                    self.stdout.write(self.style.SUCCESS(f"Fixed Arena #{arena.pk} - {arena.nome} - cloudinary URL already exists"))
                    continue
                
                # Verificar se o arquivo existe no sistema local
                if hasattr(arena.foto_quadra, 'path') and os.path.exists(arena.foto_quadra.path):
                    # Upload para o Cloudinary
                    file_name = os.path.basename(arena.foto_quadra.name)
                    base_name, ext = os.path.splitext(file_name)
                    
                    result = cloudinary.uploader.upload(
                        arena.foto_quadra.path,
                        public_id=f"cadeURacha/arenas/{base_name}",
                        overwrite=True
                    )
                    
                    # Atualizar a URL
                    arena.foto_url = result['secure_url']
                    arena.save()
                    fixed += 1
                    self.stdout.write(self.style.SUCCESS(f"Fixed Arena #{arena.pk} - {arena.nome} - uploaded local file to cloudinary"))
                    continue
                
                # Se não conseguiu encontrar o arquivo local, tentar baixar da URL
                try:
                    if hasattr(arena.foto_quadra, 'url'):
                        url = arena.foto_quadra.url
                        if url.startswith('/'):
                            url = f"http://localhost:8000{url}"  # Ajuste para o seu domínio
                            
                        response = requests.get(url, stream=True)
                        if response.status_code == 200:
                            # Salvar em um arquivo temporário
                            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                                for chunk in response.iter_content(chunk_size=1024):
                                    if chunk:
                                        tmp.write(chunk)
                                tmp_name = tmp.name
                                
                            # Upload para o Cloudinary
                            file_name = os.path.basename(arena.foto_quadra.name)
                            base_name, ext = os.path.splitext(file_name)
                            
                            try:
                                result = cloudinary.uploader.upload(
                                    tmp_name,
                                    public_id=f"cadeURacha/arenas/{base_name}",
                                    overwrite=True
                                )
                                
                                # Atualizar a URL
                                arena.foto_url = result['secure_url']
                                arena.save()
                                fixed += 1
                                self.stdout.write(self.style.SUCCESS(f"Fixed Arena #{arena.pk} - {arena.nome} - downloaded and uploaded to cloudinary"))
                            finally:
                                # Limpar arquivo temporário
                                if os.path.exists(tmp_name):
                                    os.unlink(tmp_name)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error fetching image for Arena #{arena.pk}: {str(e)}"))
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing Arena #{arena.pk}: {str(e)}"))
        
        # Caso 2: Arenas com URL direta do Cloudinary no campo foto_quadra
        cloudinary_pattern = re.compile(r'https?://res\.cloudinary\.com/')
        for arena in Arena.objects.all():
            try:
                if isinstance(arena.foto_quadra, str) and cloudinary_pattern.search(arena.foto_quadra):
                    self.stdout.write(f"Found Cloudinary URL in foto_quadra field for Arena #{arena.pk}")
                    arena.foto_url = arena.foto_quadra
                    arena.foto_quadra = None
                    arena.save()
                    fixed += 1
                    self.stdout.write(self.style.SUCCESS(f"Fixed Arena #{arena.pk} - moved URL to foto_url field"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fixing URL for Arena #{arena.pk}: {str(e)}"))
                
        self.stdout.write(self.style.SUCCESS(f'Fixed {fixed} arena images'))
    
    def _check_field_exists(self, table_name, field_name):
        """Check if a field exists in a table"""
        with connection.cursor() as cursor:
            try:
                # This works for PostgreSQL
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name=%s AND column_name=%s
                """, [table_name, field_name])
                return bool(cursor.fetchone())
            except:
                # Fallback for other databases - less accurate
                try:
                    cursor.execute(f"SELECT {field_name} FROM {table_name} LIMIT 1")
                    return True
                except:
                    return False
