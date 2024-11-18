# apps/family_legacy/models.py
from django.db import models
from django.conf import settings

class FamilyLegacy(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Meta:
    permissions = (
    ('view_family_legacy', 'Can view this family legacy'),
    ('edit_family_legacy', 'Can edit this family legacy'),
    ('share_family_legacy', 'Can share this family legacy'),
)