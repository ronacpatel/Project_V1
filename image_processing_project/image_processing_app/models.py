

from django.db import models
from django.utils import timezone
from django.contrib import admin  # Add this import
# Receipt = apps.get_model('api', 'Receipt')

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    extracted_text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)


