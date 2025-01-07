# django_project/settings.py
import os
from pathlib import Path
import environ

LOGIN_REDIRECT_URL = '/'  # Not required with a custom login view, but good as a fallback
LOGOUT_REDIRECT_URL = '/'  # Redirects to the login page after logout


# Initialize environment variables
env = environ.Env(DEBUG=(bool, False))

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Define the .env file path
env_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_path):
    environ.Env.read_env(env_path)
else:
    raise FileNotFoundError(f".env file not found at {env_path}")


# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'coreapp',  # Your app
    'debug_toolbar', # Debugging tool for development
]


# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'csp.middleware.CSPMiddleware'

]


# URL configuration
ROOT_URLCONF = 'BO.urls'   


# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Project-wide templates directory
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


# WSGI application
WSGI_APPLICATION = 'BO.wsgi.application'


# Secret key
SECRET_KEY = env('SECRET_KEY', default='your_default_secret_key')

# Secure token for webhook
ZAPIER_WEBHOOK_TOKEN = env("ZAPIER_WEBHOOK_TOKEN")

# Database configuration (to be overridden in dev/prod)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_DATABASE'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGES = [
    ('en', 'English'),
    ('pt', 'Portuguese'),
]
TIME_ZONE = 'Europe/Lisbon'
USE_I18N = True
USE_L10N = True
USE_TZ = True # ISO 8601 Compliance
DATETIME_FORMAT = 'Y-m-d\TH:i:sP'


# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Logging configuration for both dev and production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'webhook': {  # Custom logger for webhook view
            'handlers': ['console'],
            'level': 'DEBUG',  # Set to DEBUG to capture detailed logs
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',  # Logs all Django activity to console
            'propagate': False,
        },
    },
}






AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


# Email backend (SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Use your email provider's SMTP server
EMAIL_PORT = 587  # For TLS; use 465 for SSL
EMAIL_USE_TLS = True  # Enable TLS encryption
EMAIL_USE_SSL = False  # Leave False if EMAIL_USE_TLS is True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')  # Your email address
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD') # Your email password
DEFAULT_FROM_EMAIL = env('EMAIL_HOST_USER')
