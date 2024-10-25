from django.contrib import admin
from .models import FamilyLegacy

@admin.register(FamilyLegacy)
class FamilyLegacyAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'user__username')
