# apps/accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    storage_used = models.BigIntegerField(default=0)
    storage_limit = models.BigIntegerField(default=1073741824)  # 1GB
    is_deceased = models.BooleanField(default=False)
    death_verified = models.BooleanField(default=False)

    @property
    def is_online(self):
        """Check if user was active in the last 5 minutes"""
        activity = self.useractivity_set.first()
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
        return f"{self.user.email}'s activity at {self.last_activity}"

    @property
    def is_online(self):
        """Check if this activity record indicates user is online"""
        return self.last_activity >= timezone.now() - timedelta(minutes=5)