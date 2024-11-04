import os
from pathlib import Path
from django.contrib.messages import constants as messages
from dotenv import load_dotenv
import logging



WSGI_APPLICATION = 'core.wsgi.application'
ROOT_URLCONF = 'core.urls'

# Load environment variables from a .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = True

# Media files (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Where static files are collected in production
STATICFILES_DIRS = [
    BASE_DIR / "static",
]



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Third party apps
    'crispy_forms',
    'corsheaders',
    'crispy_bootstrap5',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_cleanup.apps.CleanupConfig',
    'debug_toolbar',
    'guardian',
    'ninja',  # Changed from 'ninja'
    'widget_tweaks',
    
    # Local apps
    'apps.accounts',
    'apps.content',
    'apps.family_legacy',
    'apps.dashboard',
    # Added missing comma
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'apps.accounts.middleware.UserActivityMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Specify the directory where your templates are stored
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]




# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',  # Use the 'verbose' format for detailed logging
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',  # Change to 'DEBUG' for more verbose output
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps.accounts': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'apps.content': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'apps.family_legacy': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}






AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # default
    'guardian.backends.ObjectPermissionBackend',
    'allauth.account.auth_backends.AuthenticationBackend',  # for allauth
)


# Message tags
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Security settings
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True


# Guardian Settings
GUARDIAN_RAISE_403 = True
ANONYMOUS_USER_ID = -1

SITE_ID = 1


ACCOUNT_AUTHENTICATION_METHOD = 'email'  # Use email for login
ACCOUNT_EMAIL_REQUIRED = True  # Make email mandatory for account creation
ACCOUNT_USERNAME_REQUIRED = False  # Disable username field
ACCOUNT_EMAIL_VERIFICATION = 'none'  # No email verification



EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = 'mail.therbsolutions.com'             # Your SMTP server
# EMAIL_PORT = 587                                    # Port for TLS
# EMAIL_USE_TLS = True                                # Enable TLS
# EMAIL_HOST_USER = 'test123@therbsolutions.com'      # Your InterServer email address
# EMAIL_HOST_PASSWORD = 'ak47ma41'                    # Your email account password
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER                # Default "from" email address



LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'account_login'



ACCOUNT_FORMS = {'signup': 'apps.accounts.forms.CustomSignupForm'}





# Social account providers

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# Authentication settings
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = 'account_login'


# Mailjet API configuration
MAILJET_API_KEY = '53689c5ba95e3b054a9587680bb2a0f3'         # Your actual API Key
MAILJET_API_SECRET = '3bb265b3c215af88eb4058a309b2066a'      # Your actual Secret Key
