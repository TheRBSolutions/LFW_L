from .base import *

DEBUG = False



# Security settings - keep the secret key secret in production!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')  # Make sure the environment variable is set properly.

# Using a different database (e.g., PostgreSQL) for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.your-email-provider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Static and Media file settings for production
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = '/var/www/yourdomain.com/media'

# Security settings for production
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
X_FRAME_OPTIONS = 'DENY'

ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']  # Add your production domains here


CORS_ALLOWED_ORIGINS = [
    'https://yourdomain.com',
    'https://subdomain.yourdomain.com',
    # Add other domains as needed
]
