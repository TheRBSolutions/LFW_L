from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ninja import NinjaAPI
from apps.accounts.views import router as accounts_router
from apps.content.views import router as content_router
from apps.family_legacy.views import router as family_legacy_router
from apps.accounts.views import home_view 

# Initialize Ninja API
api = NinjaAPI()

# Register routers from different apps
api.add_router('/accounts/', accounts_router)
api.add_router('/content/', content_router)
api.add_router('/family_legacy/', family_legacy_router)

# Define URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin routes for Django
    path('accounts/', include('apps.accounts.urls')),  # URL patterns for account management templates
    path('content/', include('apps.content.urls')),  # URL patterns for content management templates
    path('family_legacy/', include('apps.family_legacy.urls')),  # URL patterns for family legacy templates
    path('api/', api.urls),  # API routes for User, Content, FamilyLegacy via Ninja API,
    path('', home_view, name='home'), 
]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]