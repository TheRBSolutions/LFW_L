# apps/accounts/models.py
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class User(AbstractUser):
    # Custom fields
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    storage_used = models.BigIntegerField(default=0)
    storage_limit = models.BigIntegerField(default=1073741824)  # 1GB
    is_deceased = models.BooleanField(default=False)
    death_verified = models.BooleanField(default=False)
    trusted_devices = models.JSONField(default=list, blank=True)  # New field to store trusted devices as a list


    def save(self, *args, **kwargs):
        # Generate a unique username if it is not set
        if not self.username:
            base_username = slugify(f"{self.first_name}{self.last_name}")
            unique_username = base_username
            num = 1
            while User.objects.filter(username=unique_username).exists():
                unique_username = f"{base_username}{num}"
                num += 1
            self.username = unique_username
        super().save(*args, **kwargs)


    @property
    def is_online(self):
        """Check if user was active in the last 5 minutes"""
        activity = self.useractivity_set.first() # pylint: disable=no-member
        if activity:
            return activity.last_activity >= timezone.now() - timedelta(minutes=5)
        return False

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_activity = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'User Activities'
        ordering = ['-last_activity']  # Most recent first
        get_latest_by = 'last_activity'

    def __str__(self):
        return f"{self.user.email}'s activity at {self.last_activity}" # pylint: disable=no-member

    @property
    def is_online(self):
        """Check if this activity record indicates user is online"""
        return self.last_activity >= timezone.now() - timedelta(minutes=5)