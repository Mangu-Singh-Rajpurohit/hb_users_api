"""
Django settings for rest_users_mgmt project.

Generated by 'django-admin startproject' using Django 1.10.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os, json

dict_production_settings = {}
try:
	with open(".credentials", "r") as f_handle:
		dict_production_settings = json.load(f_handle)
except IOError:
	pass

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = dict_production_settings.get("SECRET_KEY", '#58bx$3f7=v$n#6v9&pi++qo=wfz0^306eho^07foz6ufq=ca6')

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
    'rest_framework.authtoken',
    'rest_users'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rest_users_mgmt.urls'

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

WSGI_APPLICATION = 'rest_users_mgmt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DB_VOLUME = "/db"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DB_VOLUME, 'db.sqlite3'),
    }
}


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

#   logging related settings
LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'formatters': {
      'django': {
         'format':'%(asctime)s %(name)-12s %(levelname)8s %(message)s',
       },
    },

   'handlers': {
      'FileHandler': {
         'level': 'DEBUG',
         'class': 'logging.FileHandler',
         'formatter': 'django',
         'filename': os.path.join(BASE_DIR, "server.log")
       },
       'WorkerFileHandler': {
          'level': 'DEBUG',
          'class': 'logging.FileHandler',
          'formatter': 'django',
          'filename': os.path.join(BASE_DIR, "workers.log")
       }
   },

   'loggers': {
      'root':{
         'handlers': ['FileHandler'],
         'propagate': True,
         'level': 'DEBUG',
       },
       "workers": {
       'handlers': ['WorkerFileHandler'],
       'propagate': True,
       'level': 'DEBUG',
       }
    }
}

# Rest-framework settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

# Django email settings
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = dict_production_settings.get("EMAIL_HOST_USER", None)
EMAIL_HOST_PASSWORD = dict_production_settings.get("EMAIL_HOST_PASSWORD", None)

# celery settings
CELERY_BROKER_USER_NAME = dict_production_settings.get("CELERY_BROKER_USER_NAME", "guest")
CELERY_BROKER_PASS = dict_production_settings.get("CELERY_BROKER_PASS", "guest")
CELERY_BROKER_HOST = dict_production_settings.get("CELERY_BROKER_HOST", "localhost")

CELERY_BROKER_URL = "amqp://{}:{}@{}:5672".format(CELERY_BROKER_USER_NAME, CELERY_BROKER_PASS, CELERY_BROKER_HOST)
