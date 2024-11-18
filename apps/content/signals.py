from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from guardian.shortcuts import assign_perm
from .models import Content, ContentShare, User

@receiver(post_save, sender=Content)
def assign_owner_permissions(sender, instance, created, **kwargs):
    """Assign all permissions to content creator"""
    if created:
        assign_perm('view_content', instance.user, instance)
        assign_perm('edit_content', instance.user, instance)
        assign_perm('delete_content', instance.user, instance)
        assign_perm('share_content', instance.user, instance)

@receiver(post_save, sender=User)
def handle_user_registration(sender, instance, created, **kwargs):
    """Activate pending shares when user registers"""
    if created:
        # Find pending shares for this email
        pending_shares = ContentShare.objects.filter(
            shared_with_email=instance.email,
            status='pending'
        )
        
        for share in pending_shares:
            share.shared_with = instance
            share.status = 'active'
            share.save()
            
            # Assign view permission
            assign_perm('view_content', instance, share.content)