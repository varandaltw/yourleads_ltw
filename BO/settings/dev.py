from .base import *

# Enable debug mode
DEBUG = True

# Disable security settings for local development
SECURE_SSL_REDIRECT = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Print emails to the console instead of sending them in development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Allowed hosts for development
ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='localhost, 127.0.0.1').split(',')

# Debug to ensure settings are loaded correctly
print(f"DEBUG (dev.py): DB_DATABASE={DATABASES['default']['NAME']}")

