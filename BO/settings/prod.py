from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

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
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost','yourleads_ltw.com', 'www.yourleads_ltw.com'])

# Content Security Policy
CSP_DEFAULT_SRC = ["'self'"]  # Only allow resources from your own domain
CSP_CONNECT_SRC = ["'self'", "https://hooks.zapier.com"] # API connections
CSP_SCRIPT_SRC = ["'self'", "https://zapier.com"] # No external scripts unless explicitly required
CSP_STYLE_SRC = ["'self'", "https://zapier.com"] # No external styles unless explicitly required
CSP_REPORT_ONLY = False
CSP_IMG_SRC = ["'self'", "data:"]  # Allow inline or data URIs if needed
CSP_FONT_SRC = ["'self'"]
CSP_FRAME_SRC = ["'self'"]  # No embedded frames unless explicitly required / Allow only self-hosted frames if needed
CSP_REPORT_URI = ["https://yourleads_ltw.com/csp-violations"]


# Initialize Sentry for production
sentry_sdk.init(
    dsn=env('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
    release="bo-django@1",  # Format: application@version
    environment="production",
    before_send=lambda event, hint: add_custom_tags(event),  # Add tags dynamically
)


def add_custom_tags(event, hint):
    # Access exception information from the hint
    if "exc_info" in hint:
        exception = hint["exc_info"][1]  # Exception object
        event["tags"]["exception_type"] = type(exception).__name__

    # Add custom tags
    event["tags"]["deployment_version"] = "1.2.3"
    return event

sentry_sdk.set_tag("application", "BO_Django")


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


# Debug to ensure settings are loaded correctly
print(f"DEBUG (prod.py): DB_DATABASE={DATABASES['default']['NAME']}")
