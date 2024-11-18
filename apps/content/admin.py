from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from .models import Content, ContentShare

@admin.register(Content)
class ContentAdmin(GuardedModelAdmin):
    list_display = ('title', 'user', 'content_type', 'created_at')
    list_filter = ('content_type', 'created_at')
    search_fields = ('title', 'description', 'user__email')
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(ContentShare)
class ContentShareAdmin(admin.ModelAdmin):
    list_display = ('content', 'shared_by', 'shared_with_email', 'status', 'shared_at')
    list_filter = ('status', 'shared_at')
    search_fields = ('content__title', 'shared_by__email', 'shared_with_email')
    date_hierarchy = 'shared_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'content',
            'shared_by',
            'shared_with'
        )