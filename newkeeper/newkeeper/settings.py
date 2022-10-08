"""
Django settings for newton project.

"""

import os
import sys

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_ROOT = os.path.join(BASE_DIR, "newkeeper")

# Add the individual app package path
sys.path.insert(0, os.path.join(PROJECT_ROOT, "apps"))
sys.path.insert(0, PROJECT_ROOT)

ALLOWED_HOSTS = ['*']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!nep+!kev)6+lq%1nq!k%97^w&c1^9mh*e79uj3^u&)9e=4k2!'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'werkzeug_debugger_runserver',
    'django_extensions',
    'newkeeper',
    # apps
    'api',
    'system',
    'key',
]

ROOT_URLCONF = 'newkeeper.urls'

WSGI_APPLICATION = 'newkeeper.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

# Template root directory
# TEMPLATE_DIRS = [os.path.join(PROJECT_ROOT, "templates")]

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


try:
    from settings_local import *
except Exception as inst:
    print(inst)
