import os
import time
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Clean temporary media files that are older than a specified time'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            default=1,
            type=int,
            help='Delete files older than this many days'
        )

    def handle(self, *args, **options):
        days = options['days']
        self.stdout.write(f'Cleaning temporary media files older than {days} days...')
        
        # Set cutoff time
        cutoff = time.time() - (days * 24 * 60 * 60)
        
        # Clean media directory
        media_dir = settings.MEDIA_ROOT
        count = 0
        
        try:
            for root, dirs, files in os.walk(media_dir):
                for f in files:
                    file_path = os.path.join(root, f)
                    # Skip if file is needed (e.g., default images)
                    if 'default' in f:
                        continue
                    # Check if file is older than cutoff
                    if os.path.isfile(file_path) and os.path.getmtime(file_path) < cutoff:
                        os.remove(file_path)
                        count += 1
                        self.stdout.write(f'Removed: {file_path}')
                
                # Remove empty directories
                for d in dirs:
                    dir_path = os.path.join(root, d)
                    if not os.listdir(dir_path):
                        os.rmdir(dir_path)
                        self.stdout.write(f'Removed empty directory: {dir_path}')
            
            self.stdout.write(self.style.SUCCESS(f'Successfully cleaned {count} temporary files'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error cleaning files: {str(e)}'))
