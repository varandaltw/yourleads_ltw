import sentry_sdk
from .base import *
from sentry_sdk.integrations.django import DjangoIntegration

# Enable debug mode
DEBUG = True

# Disable security settings for local development
SECURE_SSL_REDIRECT = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Print emails to the console instead of sending them in development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')


# Allowed hosts for development
ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='localhost, 127.0.0.1').split(',')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Modify logging for development
LOGGING['loggers']['django']['handlers'] = ['console']
LOGGING['loggers']['django']['level'] = 'DEBUG'

LOGGING['loggers']['custom_logger']['handlers'] = ['console']
LOGGING['loggers']['custom_logger']['level'] = 'DEBUG'

LOGGING['loggers']['webhook']['handlers'] = ['console']
LOGGING['loggers']['webhook']['level'] = 'DEBUG'

sentry_sdk.init(
    dsn=env('SENTRY_DSN', default=''),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,  # Low sample rate for development
    send_default_pii=True,
)

# Use relaxed CSP settings for development
CSP_REPORT_ONLY = True  # Enable reporting mode for CSP debugging
CSP_SCRIPT_SRC.extend(["'unsafe-inline'", "'unsafe-eval'"])  # Allow unsafe scripts in dev

# Debug to ensure settings are loaded correctly
print(f"DEBUG (dev.py): DB_DATABASE={DATABASES['default']['NAME']}")
