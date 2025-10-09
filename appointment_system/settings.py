# appointment_system/settings.py

import os
from pathlib import Path
import environ  # Import the environ library

# Initialize environment variables
env = environ.Env(
    # Set casting, default value
    DEBUG=(bool, True),
    # Default to SQLite for local development
    DATABASE_URL=(str, f"sqlite:///{Path(__file__).resolve().parent.parent / 'db.sqlite3'}"),
    # Default to current insecure key, but env() will override if set in .env
    SECRET_KEY=(str, 'django-insecure-aqmw)l1&#-itk245)k701bscmt(g!%5ie3b4c%t%9q+v$pc_+5'),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env file (if it exists)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# --- Core Settings ---
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

# Set ALLOWED_HOSTS for GitPod/production
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'] if DEBUG else [])
#CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[] if DEBUG else ['https://*.render.com'])
CSRF_TRUSTED_ORIGINS = [
    # Allow all GitPod workspaces (RECOMMENDED)
    'https://*.gitpod.io',
    # Optionally, add your exact current URL for absolute certainty
    'https://8000-hate19991-newvision-i1o8vaok919.ws-eu121.gitpod.io',
]


# Application definition

INSTALLED_APPS = [
    # Required Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # REQUIRED by allauth

    # Third-party DRF & Auth apps
    'rest_framework',
    'rest_framework.authtoken',  # Token auth for DRF
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',  # Google Auth
    'dj_rest_auth',
    'dj_rest_auth.registration',
     'corsheaders', 

    # Local app
    'core',  # Your application containing User, Appointment, and Message models
]

SITE_ID = 1  # Required by django.contrib.sites
# appointment_system/settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'allauth.account.middleware.AccountMiddleware', 
    
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'appointment_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request', # REQUIRED by allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'appointment_system.wsgi.application'


# --- Database Configuration ---
# Uses django-environ to read DATABASE_URL (Postgres on Render, SQLite locally)
DATABASES = {
    'default': env.db(),
}


# Password validation (keep defaults)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- Custom User Model ---
AUTH_USER_MODEL = 'core.User'


# --- Django REST Framework (DRF) Settings ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # Token authentication is standard for DRF APIs
        'rest_framework.authentication.TokenAuthentication', 
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# --- DJ-REST-AUTH Settings ---
REST_AUTH = {
    'USE_JWT': False,
    'USER_DETAILS_SERIALIZER': 'core.serializers.UserDetailsSerializer',
    'SESSION_LOGIN': False, # Recommended for API only setup
}

# --- Allauth/Social Login Settings ---
AUTHENTICATION_BACKENDS = (
    # Default Django backend
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_LOGIN_METHODS = ['email'] 
ACCOUNT_EMAIL_VERIFICATION = 'none' # Set to 'mandatory' in production
LOGIN_REDIRECT_URL = '/'

# Google Provider Configuration (Load credentials from .env)
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': env('GOOGLE_CLIENT_ID', default='DUMMY_CLIENT_ID'),
            'secret': env('GOOGLE_SECRET', default='DUMMY_SECRET'),
            'key': ''
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}


# --- CORS (Cross-Origin Resource Sharing) Settings ---
# Allows a separate frontend application (e.g., React/Vue) to access the API
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Allow all in DEBUG (dev), but limit in production

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    # Add your frontend URLs here for production
])


# --- Static Files (Deployment) ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'