import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '-05sgp9!deq=q1nltm@^^2cc+v29i(tyybv3v2t77qi66czazj'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'corsheaders',
    'model_clone',
    # 'rest_auth',
    # 'rest_auth.registration',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'bulma',

    'core',
    'dashboard',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'home.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'  # For US timezone : UTC
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'build/static')]
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    '/var/www/static/',
]
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_cdn")
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGOUT_ON_GET = True
