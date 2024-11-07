import os
from pathlib import Path
import mimetypes
from datetime import timedelta
import sqlite3

from django.core.exceptions import AppRegistryNotReady

try:
    from core_modules.app_configurator.models import AppConfigurator
except AppRegistryNotReady:
    AppConfigurator = None

from .specific import PRODUCTION

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    from .specific import SECRET_KEY
except ImportError:
    SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
try:
    from .specific import DEBUG
except ImportError:
    DEBUG = True

try:
    from .specific import ALLOWED_HOSTS
except ImportError:
    ALLOWED_HOSTS = ['*']

if PRODUCTION == False:
    CORS_ORIGIN_ALLOW_ALL = True

    CORS_ALLOW_CREDENTIALS = True

    CORS_ALLOW_METHODS = [
        "DELETE",
        "GET",
        "OPTIONS",
        "PATCH",
        "POST",
        "PUT",
    ]
    CORS_ALLOW_HEADERS = [
        "accept",
        "accept-encoding",
        "authorization",
        "content-type",
        "dnt",
        "origin",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
    ]


# Application definition
def get_enabled_apps():
    try:
        from django.apps import apps
        if not apps.ready:
            return []
        from core_modules.app_configurator.models import AppConfigurator
        return [app.name for app in AppConfigurator.objects.filter(enabled=True)]
    except (AppRegistryNotReady, ImportError) as e:
        print("Error while loading enabled apps:", e)
        return []


DJANGO_MODULES = ['django.contrib.admin',
                  'django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.messages',
                  'django.contrib.staticfiles',
                  'drf_yasg',
                  'rest_framework',
                  'corsheaders']

CORE_MODULES = ['core_modules.user_manager',
                'core_modules.testing',
                'core_modules.app_configurator']

CUSTOM_MODULES = get_enabled_apps()

INSTALLED_APPS = DJANGO_MODULES + CORE_MODULES + CUSTOM_MODULES

if PRODUCTION == True:
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
else:
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

ROOT_URLCONF = 'edplatform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'edplatform.wsgi.application'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 13000

AUTH_USER_MODEL = 'user_manager.User'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if PRODUCTION == True:
    try:
        from .specific import DATABASES
    except ImportError:
        DATABASES = {}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'user_manager.backends.JWTAuthentication',
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

try:
    from .specific import JWT_SECRET_KEY
except ImportError:
    JWT_SECRET_KEY = ""

try:
    from .specific import EMAIL_BACKEND
    from .specific import EMAIL_USE_TLS
    from .specific import EMAIL_HOST
    from .specific import EMAIL_HOST_USER
    from .specific import EMAIL_HOST_PASSWORD
    from .specific import EMAIL_PORT
except ImportError:
    EMAIL_BACKEND = ""
    EMAIL_USE_TLS = ""
    EMAIL_HOST = ""
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    EMAIL_PORT = ""

try:
    from .specific import AWS_S3_ACCESS_KEY_ID
    from .specific import AWS_S3_SECRET_ACCESS_KEY
    from .specific import AWS_STORAGE_BUCKET_NAME

    from .specific import AWS_S3_FILE_OVERWRITE
    from .specific import AWS_DEFAULT_ACL
    from .specific import DEFAULT_FILE_STORAGE
    from .specific import AWS_S3_ENDPOINT_URL

    from .specific import AWS_S3_REGION_NAME
    from .specific import AWS_S3_SIGNATURE_VERSION

except ImportError:
    AWS_S3_ACCESS_KEY_ID = ""
    AWS_S3_SECRET_ACCESS_KEY = ""
    AWS_STORAGE_BUCKET_NAME = ""

    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_S3_ENDPOINT_URL = ""

    AWS_S3_REGION_NAME = 'eu-south-1'  # change to your region
    AWS_S3_SIGNATURE_VERSION = 's3v4'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
