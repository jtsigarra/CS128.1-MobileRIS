import os
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Creates necessary media folders for the application'
    
    def handle(self, *args, **options):
        folders = [
            settings.MEDIA_ROOT,
            os.path.join(settings.MEDIA_ROOT, 'dicom_files'),
            os.path.join(settings.MEDIA_ROOT, 'patient_photos'),
            os.path.join(settings.MEDIA_ROOT, 'reports'),
            os.path.join(settings.MEDIA_ROOT, 'temp_uploads'),
        ]
        
        self.stdout.write("Setting up media folders...")
        
        for folder in folders:
            try:
                os.makedirs(folder, exist_ok=True)
                self.stdout.write(self.style.SUCCESS(f'✓ Created/verified folder: {folder}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Failed to create folder {folder}: {e}'))
