from django.contrib import admin
from .models import Content

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'content_type', 'created_at')
    list_filter = ('content_type', 'created_at')
    search_fields = ('title', 'user__username')
