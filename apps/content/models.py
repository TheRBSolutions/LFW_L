# apps/content/models.py
from django.db import models
from django.conf import settings

def content_file_path(instance, filename):
    return f'content/{instance.user.id}/{filename}'

class Content(models.Model):
    CONTENT_TYPES = [
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('image', 'Image'),
        ('note', 'Note'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    file = models.FileField(upload_to=content_file_path)
    size = models.BigIntegerField(editable=False)
    exclude_from_legacy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)