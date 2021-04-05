"""
Django settings for HelloWorld project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import rest_framework
import logging
from logging.handlers import TimedRotatingFileHandler
from HelloWorld.secret import secret
import platform

IS_UNIX = False if "Windows" in platform.platform() else True

# Build Log Setting 
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler('Log/Service.log', when = 'd', interval = 1, backupCount=10)
handler.setFormatter(logging.Formatter('[%(asctime)s] %(filename)s [%(levelname)s] :%(message)s'))
logger.addHandler(handler)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret.SECRET_KEY
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'HelloWorld.Book',
    'HelloWorld.User'
]

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES':[
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'HelloWorld.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'Templates')],
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

WSGI_APPLICATION = 'HelloWorld.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': { 
        'ENGINE': 'django.db.backends.mysql',
        'NAME': secret.MYSQL_DATABASE, 
        'HOST': secret.MYSQL_HOST, 
        'PORT': secret.MYSQL_PORT,
        'USER': secret.MYSQL_USER,
        'PASSWORD': secret.MYSQL_PW,
    } 
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}".format(secret.REDIS_HOST,secret.REDIS_PORT),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
            # "PASSWORD": "密码",
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/' # 别名 
MEDIA_ROOT = os.path.join(BASE_DIR, "Statics")
STATICFILES_DIRS = [ 
    os.path.join(BASE_DIR, "Statics"), 
]

# FILE PATH Settings
COVER_SIZE = (800, 1200)
PDF_INPUT_PATH = "Statics/bookData/"
IMAGE_OUTPUT_PATH = "Statics/image/pdf_cover/"

# URI PATH Settings
PDF_COVER_PATH = STATIC_URL + "image/pdf_cover/"

