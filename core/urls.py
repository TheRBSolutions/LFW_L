# core/urls.py
import debug_toolbar # pylint: disable=import-error
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ninja import NinjaAPI # pylint: disable=import-error
from apps.dashboard.api import router as dashboard_router
from apps.accounts.views import home_view
from .api import api  # Import the API instance from core/api.py
from django.contrib.auth.views import LogoutView
from views import CustomAdminLogoutView  # Import the view from the root directory





urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/logout/', CustomAdminLogoutView.as_view(), name='custom_admin_logout'),  # Custom admin logout

    
    # Move accounts URL to beginning to ensure proper routing
    path('accounts/', include('apps.accounts.urls')),  # Changed from 'accounts/' to ''
    path('content/', include('apps.content.urls')),
    path('family_legacy/', include('apps.family_legacy.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('api/', api.urls),
    path('', home_view, name='home'),
    path("__reload__/", include("django_browser_reload.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]