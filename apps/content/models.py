from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
from guardian.shortcuts import assign_perm
import uuid
import os

User = get_user_model()

def content_file_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('content', str(instance.user.id), unique_filename)

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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ('can_view_shared_content', 'Can view shared content'),
            ('can_edit_shared_content', 'Can edit shared content'),
            ('can_delete_shared_content', 'Can delete shared content'),
            ('can_share_content', 'Can share content'),
        )

    def save(self, *args, **kwargs):
        if self.file:
            self.size = self.file.size
        super().save(*args, **kwargs)

    def share_with_email(self, email, shared_by):
        """Share content with user by email"""
        try:
            # Check if user exists
            user = User.objects.get(email=email)
            
            # Create share for existing user
            share = ContentShare.objects.create(
                content=self,
                shared_by=shared_by,
                shared_with=user,
                shared_with_email=email,
                status='active'
            )
            
            # Assign view permission
            assign_perm('view_content', user, self)
            
            # Send notification
            send_mail(
                'Content Shared With You',
                f'''{shared_by.get_full_name()} has shared "{self.title}" with you.
                You can now access this content in your dashboard.''',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
            
        except User.DoesNotExist:
            # Create pending share for new user
            share = ContentShare.objects.create(
                content=self,
                shared_by=shared_by,
                shared_with_email=email,
                status='pending',
                invitation_token=uuid.uuid4().hex
            )
            
            # Send invitation
            invitation_link = f"{settings.SITE_URL}/register/?token={share.invitation_token}"
            send_mail(
                'Invitation to Access Shared Content',
                f'''Hello!
                {shared_by.get_full_name()} wants to share "{self.title}" with you.
                To access this content, please register here:
                {invitation_link}
                ''',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
            
        return share

class ContentShare(models.Model):
    SHARE_STATUS = [
        ('pending', 'Pending Registration'),
        ('active', 'Active'),
        ('expired', 'Expired'),
    ]

    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='shares')
    shared_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='shared_content'
    )
    shared_with = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_shares',
        null=True,
        blank=True
    )
    shared_with_email = models.EmailField()
    status = models.CharField(max_length=20, choices=SHARE_STATUS, default='pending')
    shared_at = models.DateTimeField(auto_now_add=True)
    invitation_token = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        unique_together = ('content', 'shared_with_email')
        ordering = ('-shared_at',)