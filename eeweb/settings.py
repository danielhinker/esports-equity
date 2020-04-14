"""
Django settings for eeweb project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
Online = True

ALLOWED_HOSTS = ['eeweb-test.us-east-1.elasticbeanstalk.com', 'www.esportsequity.com', 'esportsequity.com',
                 'prototype.esportsequity.com', '*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'rest_framework',
    'allauth',
    'allauth.account',
     'allauth.socialaccount',
     'allauth.socialaccount.providers.github',
    'teams',
    'bootstrap3',
    'accounts',
    'transact',
    'stripe_api',
    'storages',
    'admin_honeypot',
    'widget_tweaks',
    'stripe',
    'jquery_ui',
    'django_ses',
    'boto3',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware'
]

SECURE_SSL_HOST = True

ROOT_URLCONF = 'eeweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
            ],
        },
    },
]

ACCOUNT_USER_MODEL_EMAIL_FIELD = 'username'

WSGI_APPLICATION = 'eeweb.wsgi.application'

DATE_INPUT_FORMATS = ('%m-%d-%Y',)

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

if not Online:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }



else:
    import dj_database_url

    DATABASES = { 'default': dj_database_url.config() }

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Pacific'

USE_I18N = True

USE_L10N = False

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/


clientID = os.environ['clientID']

developerAPIKey = os.environ['developerAPIKey']
APIKEY = {'clientID': clientID, 'developerAPIKey': developerAPIKey}
AUTH_USER_MODEL = "accounts.User"
client_secret = os.environ['client_secret']

AUTHENTICATION_BACKENDS = (
	"django.contrib.auth.backends.ModelBackend",
	"allauth.account.auth_backends.AuthenticationBackend",
)

if Online:
    SITE_ID = 4
else:
    SITE_ID = 5

ADMIN_MEDIA_PREFIX = '/media/'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)
MEDIA_URL = '/media/'

# IAM User
# ACCESS_ID = os.environ['ACCESS_ID']
# ACCESS_KEY = os.environ['ACCESS_KEY']
#
# AWS_ACCESS_KEY_ID = os.environ['ACCESS_ID']
# AWS_SECRET_ACCESS_KEY = os.environ['ACCESS_KEY']
# AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
# S3_URL = 'https://%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_DEFAULT_REGION = os.environ['AWS_DEFAULT_REGION']
#
# ACCOUNT_EMAIL_SUBJECT_PREFIX = 'Esports Equity '

# if Online:
#
#     MEDIA_URL = S3_URL + '/media/'
#     AWS_QUERYSTRING_AUTH = False
#     CSRF_COOKIE_SECURE = True
#     SESSION_COOKIE_SECURE = True
#     SECURE_SSL_REDIRECT = True
#     AWS_S3_SECURE_URLS = True
#     DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#     STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#
#     SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# if Online:
#     EMAIL_BACKEND = os.environ['EMAIL_BACKEND']
#     EMAIL_HOST = os.environ['EMAIL_HOST']
#     EMAIL_PORT = os.environ['EMAIL_PORT']
#     EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
#     EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
# else:
#     EMAIL_BACKEND = os.environ['OFFLINE_EMAIL_BACKEND']
#     EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
