import os
from django.core.management.base import BaseCommand
import re
from app_synes.models import Jogo
import cloudinary
import cloudinary.uploader
from django.conf import settings
import tempfile
import requests
from django.db import connection

class Command(BaseCommand):
    help = 'Fix racha images URLs for Cloudinary'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Racha image fixes for Cloudinary'))
        
        # First, check if foto_url field exists
        has_foto_url = self._check_field_exists('app_synes_jogo', 'foto_url')
        
        if not has_foto_url:
            self.stdout.write(self.style.WARNING('The foto_url field does not exist in Jogo model. Please run migrations first.'))
            return
        
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
            api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
            api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
            secure=True
        )
        
        # Count of fixed rachas
        fixed = 0
        
        # Caso 1: Rachas com imagem mas sem foto_url
        jogos = Jogo.objects.filter(imagem__isnull=False).exclude(imagem='').filter(foto_url__isnull=True)
        self.stdout.write(f"Found {jogos.count()} rachas with imagem but no foto_url")
        
        for jogo in jogos:
            try:
                # Verificar se a URL já é do Cloudinary 
                if hasattr(jogo.imagem, 'url') and 'res.cloudinary.com' in jogo.imagem.url:
                    jogo.foto_url = jogo.imagem.url
                    jogo.save()
                    fixed += 1
                    self.stdout.write(self.style.SUCCESS(f"Fixed Jogo #{jogo.pk} - {jogo.titulo} - cloudinary URL already exists"))
                    continue
                
                # Verificar se o arquivo existe no sistema local
                if hasattr(jogo.imagem, 'path') and os.path.exists(jogo.imagem.path):
                    # Upload para o Cloudinary
                    file_name = os.path.basename(jogo.imagem.name)
                    base_name, ext = os.path.splitext(file_name)
                    
                    result = cloudinary.uploader.upload(
                        jogo.imagem.path,
                        public_id=f"cadeURacha/rachas/{base_name}",
                        overwrite=True
                    )
                    
                    # Atualizar a URL
                    jogo.foto_url = result['secure_url']
                    jogo.save()
                    fixed += 1
                    self.stdout.write(self.style.SUCCESS(f"Fixed Jogo #{jogo.pk} - {jogo.titulo} - uploaded local file to cloudinary"))
                    continue
                
                # Se não conseguiu encontrar o arquivo local, tentar baixar da URL
                try:
                    if hasattr(jogo.imagem, 'url'):
                        url = jogo.imagem.url
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
                            file_name = os.path.basename(jogo.imagem.name)
                            base_name, ext = os.path.splitext(file_name)
                            
                            try:
                                result = cloudinary.uploader.upload(
                                    tmp_name,
                                    public_id=f"cadeURacha/rachas/{base_name}",
                                    overwrite=True
                                )
                                
                                # Atualizar a URL
                                jogo.foto_url = result['secure_url']
                                jogo.save()
                                fixed += 1
                                self.stdout.write(self.style.SUCCESS(f"Fixed Jogo #{jogo.pk} - {jogo.titulo} - downloaded and uploaded to cloudinary"))
                            finally:
                                # Limpar arquivo temporário
                                if os.path.exists(tmp_name):
                                    os.unlink(tmp_name)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error fetching image for Jogo #{jogo.pk}: {str(e)}"))
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing Jogo #{jogo.pk}: {str(e)}"))
        
        # Caso 2: Jogos com URL direta do Cloudinary no campo imagem
        cloudinary_pattern = re.compile(r'https?://res\.cloudinary\.com/')
        for jogo in Jogo.objects.all():
            try:
                if isinstance(jogo.imagem, str) and cloudinary_pattern.search(jogo.imagem):
                    self.stdout.write(f"Found Cloudinary URL in imagem field for Jogo #{jogo.pk}")
                    jogo.foto_url = jogo.imagem
                    jogo.imagem = None
                    jogo.save()
                    fixed += 1
                    self.stdout.write(self.style.SUCCESS(f"Fixed Jogo #{jogo.pk} - moved URL to foto_url field"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fixing URL for Jogo #{jogo.pk}: {str(e)}"))
                
        self.stdout.write(self.style.SUCCESS(f'Fixed {fixed} racha images'))
    
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
