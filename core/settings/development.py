from .base import *

DEBUG = True

ALLOWED_HOSTS = ['lfwlatest-production.up.railway.app','localhost', '127.0.0.1']

INTERNAL_IPS = [
    "127.0.0.1",
]

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Emails are printed in console during development

# Additional or modified settings for development can go here.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Development settings
CORS_ALLOW_ALL_ORIGINS = True  # Only in development
