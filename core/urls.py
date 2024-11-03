# core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ninja import NinjaAPI
from apps.dashboard.api import router as dashboard_router
from apps.accounts.views import home_view

# Initialize Ninja API
api = NinjaAPI()
api.add_router("/dashboard/", dashboard_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # All authentication views handled in accounts app
    path('accounts/', include('apps.accounts.urls')),  # All auth (custom + Google)

    # Other app URLs
    path('content/', include('apps.content.urls')),
    path('family_legacy/', include('apps.family_legacy.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('api/', api.urls),
    path('', home_view, name='home'),  # Home view
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
