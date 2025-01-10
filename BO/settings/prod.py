from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Debug to ensure settings are loaded correctly
print(f"DEBUG (prod.py): DB_DATABASE={DATABASES['default']['NAME']}")

DEBUG = False

# Production-specific security settings
SECRET_KEY = env('SECRET_KEY')

SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'


ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['yourleads_ltw.com', 'www.yourleads_ltw.com'])

# Content Security Policy
CSP_DEFAULT_SRC = ["'self'"]  # Only allow resources from your own domain
CSP_CONNECT_SRC = ["'self'", "https://hooks.zapier.com"] # API connections
CSP_SCRIPT_SRC = ["'self'", "https://zapier.com"] # No external scripts unless explicitly required
CSP_STYLE_SRC = ["'self'", "https://zapier.com"] # No external styles unless explicitly required
CSP_REPORT_ONLY = True
CSP_IMG_SRC = ["'self'", "data:"]  # Allow inline or data URIs if needed
CSP_FONT_SRC = ["'self'"]
CSP_FRAME_SRC = ["'self'"]  # No embedded frames unless explicitly required
CSP_REPORT_URI = ["https://yourleads_ltw.com/csp-violations"]

# Initialize Sentry for production
sentry_sdk.init(
    dsn=env('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

# Logging for production
LOGGING['loggers']['django']['handlers'] = ['console', 'error_file']
LOGGING['loggers']['django']['level'] = 'ERROR'

LOGGING['loggers']['custom_logger']['handlers'] = ['console', 'info_file']
LOGGING['loggers']['custom_logger']['level'] = 'INFO'

LOGGING['loggers']['webhook']['handlers'] = ['console', 'warning_file', 'error_file']
LOGGING['loggers']['webhook']['level'] = 'WARNING'

LOGGING['handlers']['sentry'] = {
    'level': 'ERROR',
    'class': 'sentry_sdk.integrations.logging.EventHandler',
}
LOGGING['loggers']['django']['handlers'].append('sentry')  # Add Sentry for error monitoring
LOGGING['loggers']['webhook']['handlers'].append('sentry')
