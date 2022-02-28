"""
Django settings for archive project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

from lcogt_logging import LCOGTFormatter
from ocs_archive.settings.settings import get_tuple_from_environment

import ast
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'e7#jz9=op7b14zqsxhj^svei4*r0t+^se^xhb-()&s_dlgvc!k')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ast.literal_eval(os.getenv('DEBUG', 'False'))

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'rest_framework',
    'rest_framework.authtoken',
    'ocs_authentication.auth_profile',
    'django_filters',
    'corsheaders',
    'crispy_forms',
    'django_extensions',
    'archive.frames',
    'archive.authentication',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'ocs_authentication.backends.OAuthUsernamePasswordBackend',
]

ROOT_URLCONF = 'archive.urls'

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

WSGI_APPLICATION = 'archive.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
# https://docs.djangoproject.com/en/2.2/topics/db/multi-db/#automatic-database-routing

DATABASE_ROUTERS = ['archive.dbrouters.DBClusterRouter']

DB_NAME = os.getenv('DB_NAME', 'archive')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'postgres')

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
    },
    'replica': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': os.getenv('DB_HOST_READER', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            '()': LCOGTFormatter
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = '/static/'
STATIC_URL = '/static/'

MEDIA_ROOT = '/media/'
MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'ocs_authentication.backends.OCSTokenAuthentication',  # Allows authentication against Oauth Servers api_token
        'rest_framework.authentication.SessionAuthentication',
        'archive.authentication.backends.BearerAuthentication',  # Allows auth using oauth bearer
    ),
    'DEFAULT_PAGINATION_CLASS': 'archive.frames.pagination.LimitedLimitOffsetPagination',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'archive.authentication.throttling.AllowStaffUserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10000/day',
        'user': '50000/day',
    },
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'archive.renderers.CustomBrowsableAPIRenderer',
    )
}

# This project now requires connection to an OAuth server for authenticating users to make changes
# In the OCS, this would be the Observation Portal backend
OCS_AUTHENTICATION = {
    'OAUTH_TOKEN_URL': os.getenv('OAUTH_TOKEN_URL', 'http://127.0.0.1:8000/o/token/'),
    'OAUTH_PROFILE_URL': os.getenv('OAUTH_PROFILE_URL', 'http://127.0.0.1:8000/api/profile/'),
    'OAUTH_CLIENT_ID': os.getenv('OAUTH_CLIENT_ID', ''),
    'OAUTH_CLIENT_SECRET': os.getenv('OAUTH_CLIENT_SECRET', ''),
    'OAUTH_SERVER_KEY': os.getenv('OAUTH_SERVER_KEY', ''),
    'REQUESTS_TIMEOUT_SECONDS': 60
}

CORS_ORIGIN_ALLOW_ALL = True

if os.getenv('CACHE_LOC', None) is not None:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': os.getenv('CACHE_LOC', 'memcached.archiveapi:11211'),
        }
    }

# Settings pertaining to posting messages to the post archived fits exchange
QUEUE_BROKER_URL = os.getenv('QUEUE_BROKER_URL', 'memory://localhost')
PROCESSED_EXCHANGE_ENABLED = ast.literal_eval(os.getenv('PROCESSED_EXCHANGE_ENABLED', 'True'))
PROCESSED_EXCHANGE_NAME = os.getenv('PROCESSED_EXCHANGE_NAME', 'archived_fits')

# Settings for available configuration_types: use configdb if available, otherwise fall back on direct setting
CONFIGDB_URL = os.getenv('CONFIGDB_URL', '')
CONFIGURATION_TYPES = get_tuple_from_environment('CONFIGURATION_TYPES', 'BIAS,DARK,EXPOSE,SPECTRUM,LAMPFLAT,SKYFLAT,STANDARD,TRAILED,GUIDE,EXPERIMENTAL,CATALOG')

# Additional Customization
ZIP_DOWNLOAD_FILENAME_BASE = os.getenv('ZIP_DOWNLOAD_FILENAME_BASE', 'ocs_archive_data')
ZIP_DOWNLOAD_MAX_UNCOMPRESSED_FILES = int(os.getenv('ZIP_DOWNLOAD_MAX_UNCOMPRESSED_FILES', 10))
NAVBAR_TITLE_TEXT = os.getenv('NAVBAR_TITLE_TEXT', 'Science Archive API')
NAVBAR_TITLE_URL = os.getenv('NAVBAR_TITLE_URL', 'https://archive.lco.global')
TERMS_OF_SERVICE_URL = os.getenv('TERMS_OF_SERVICE_URL', 'https://lco.global/policies/terms/')
DOCUMENTATION_URL = os.getenv('DOCUMENTATION_URL', 'https://observatorycontrolsystem.github.io/api/science_archive/')
PAGINATION_DEFAULT_LIMIT = int(os.getenv('PAGINATION_DEFAULT_LIMIT', 100))
PAGINATION_MAX_LIMIT = int(os.getenv('PAGINATION_MAX_LIMIT', 1000))

try:
    from .local_settings import *
except ImportError:
    pass

try:
    INSTALLED_APPS += LOCAL_INSTALLED_APPS  # noqa
    ALLOWED_HOSTS += LOCAL_ALLOWED_HOSTS  # noqa
except:
    pass
