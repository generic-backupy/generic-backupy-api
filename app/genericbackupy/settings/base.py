"""
Django settings for genericbackupy project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta
from rest_framework.settings import api_settings
import firebase_admin

PRIVACY_VERSION = "0.0.1"
CONDITIONS_VERSION = "0.0.1"
API_VERSION = "0.0.1"

firebase_admin.initialize_app()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'corsheaders',
    'rest_framework',
    'knox',
    'django_filters',
    'django_q',
    'django_rq',
    'django_nose'
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
    'django.middleware.locale.LocaleMiddleware',
    #'api.middlewares.ContractVersionMiddleware'
]

ROOT_URLCONF = 'genericbackupy.urls'

AUTH_USER_MODEL = 'api.User'

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

WSGI_APPLICATION = 'genericbackupy.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#database
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genericbackupy.settings')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
        'TEST': {
            'NAME': 'testdatabase',
        },
    }
}

# SMTP Server
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = os.environ.get('SMTP_HOST')
EMAIL_PORT = 465
EMAIL_HOST_USER = os.environ.get('SMTP_USER')
EMAIL_HOST_PASSWORD = os.environ.get('SMTP_PASSWORD')

# EMAIL SETTINGS
EMAIL_DEFAULT_SENDER = os.environ.get('EMAIL_DEFAULT_SENDER', 'Generic Backupy <app@generic-backupy.at>')

# VERIFY BASE URL
VERIFY_EMAIL_URL = os.environ.get('VERIFY_EMAIL_URL')
RESET_PASSWORD_URL = os.environ.get('RESET_PASSWORD_URL')

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
        'knox.auth.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.CustomPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/minute',
        'user': '200/minute'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.normpath(os.path.join(BASE_DIR, "static/admin")),
    os.path.normpath(os.path.join(BASE_DIR, "static/rest_framework")),
)

# CORS Setup
# https://github.com/ottoyiu/django-cors-headers

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
)
CORS_EXPOSE_HEADERS = (
    'Filename',
    'Content-Type',
    'Content-Disposition'
)

REST_KNOX = {
    'TOKEN_TTL': timedelta(days=90),
    'AUTO_REFRESH': True,
    'MIN_REFRESH_INTERVAL': 1*60
}

# Configure your Q cluster
# More details https://django-q.readthedocs.io/en/latest/configure.html
Q_CLUSTER = {
    "name": "dh",
    "orm": "default",  # Use Django's ORM + database for broker
}

RQ_QUEUES = {
    'default': {
        'HOST': os.environ.get('REDIS_HOST'),
        'PORT': os.environ.get('REDIS_PORT'),
        'DB': os.environ.get('REDIS_DB'),
        'PASSWORD': os.environ.get('REDIS_PASSWORD'),
        'DEFAULT_TIMEOUT': os.environ.get('RQ_DEFAULT_TIMEOUT'),
        "SSL": (os.environ.get('REDIS_TLS_ENABLED') or "False").lower() in ["true", "yes", "1"]
    }
}
