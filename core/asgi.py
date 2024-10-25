# import os
# from django.core.asgi import get_asgi_application
# from dotenv import load_dotenv
# Load environment variables from a .env file
# load_dotenv()

# # Set DJANGO_ENV to either 'development' or 'production'
# env = os.getenv('DJANGO_ENV', 'development')

# # Use the appropriate settings module based on the environment
# if env == 'production':
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')
# else:
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')

# application = get_asgi_application()
