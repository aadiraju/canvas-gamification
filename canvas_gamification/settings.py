"""
Django settings for canvas_gamification project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from django.contrib.messages import constants as message_constants
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.urls import reverse_lazy

from canvas_gamification.env import read_env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=cv^=w$b8iw4q5!ti#j)mxwujw24o)_d*og7($erv@4t5=3z7*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'true') == 'true'
HEROKU = False

if DEBUG:
    read_env(os.path.join(BASE_DIR, 'env', 'gamification.dev.env'))

if HEROKU:
    ALLOWED_HOSTS = ['canvas-gamification.herokuapp.com']
elif DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = os.environ['SERVER_NAME'].split()

# Load YouTube Keys for Video Recommendations
read_env(os.path.join(BASE_DIR, 'env', 'videorecs.env'))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_filters',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'djrichtextfield',
    'accounts',
    'course',
    'jsoneditor',
    'general',
    'api',
    'canvas',
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
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'accounts.middlewares.login_overlay_middleware',
]

ROOT_URLCONF = 'canvas_gamification.urls'

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

WSGI_APPLICATION = 'canvas_gamification.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            'TEST': {
                'NAME': os.path.join(BASE_DIR, 'db_test.sqlite3'),
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get("POSTGRES_DB", "postgres"),
            'USER': os.environ.get("POSTGRES_USER", "postgres"),
            'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
            'HOST': os.environ.get("POSTGRES_HOST", "db"),
            'PORT': os.environ.get("POSTGRES_PORT", 5432),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Canada/Pacific'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}

DJRICHTEXTFIELD_CONFIG = {
    'js': ['/static/ckeditor/ckeditor.js'],
    'init_template': 'djrichtextfield/init/ckeditor.js',
    'profiles': {
        'basic': {
            'toolbar': [
                {'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'CopyFormatting',
                           'RemoveFormat']},
                {'items': ['Link', 'CodeSnippet', 'Code', 'base64image', 'Mathjax', 'SpecialChar']},
                {'items': ['Styles', 'Format', 'Font', 'FontSize']},
                {'items': ['Source']}
            ],
            'format_tags': 'p;h1;h2;h3',
            'extraPlugins': ['codesnippet', 'codeTag', 'base64image'],
            'mathJaxLib': '//cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-AMS_HTML',
        },
        'advanced': {
            'extraPlugins': ['codesnippet', 'codeTag', 'base64image'],
            'mathJaxLib': '//cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-AMS_HTML',
        },
    }
}

MESSAGE_TAGS = {message_constants.ERROR: 'danger'}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

AUTH_USER_MODEL = 'accounts.MyUser'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

LOGIN_URL = reverse_lazy('accounts:login')
LOGOUT_URL = reverse_lazy('accounts:logout')
LOGIN_REDIRECT_URL = reverse_lazy('homepage')
LOGOUT_REDIRECT_URL = reverse_lazy('homepage')

if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_ACTIVATION = "test@gamification.com"
    EMAIL_PASSWORD_RESET = "test@gamification.com"
else:
    EMAIL_USE_TLS = os.environ['EMAIL_USE_TLS']
    EMAIL_HOST = os.environ['EMAIL_HOST']
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    EMAIL_PORT = os.environ['EMAIL_PORT']
    EMAIL_ACTIVATION = os.environ['EMAIL_ACTIVATION']
    EMAIL_PASSWORD_RESET = os.environ['EMAIL_PASSWORD_RESET']
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

JUDGE0_HOST = os.environ['JUDGE0_HOST']
JUDGE0_PASSWORD = os.environ['JUDGE0_PASSWORD']

if DEBUG:
    RECAPTCHA_KEY = ""
    RECAPTCHA_URL = ""
else:
    RECAPTCHA_KEY = os.environ['RECAPTCHA_KEY']
    RECAPTCHA_URL = os.environ['RECAPTCHA_URL']

if HEROKU:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    import dj_database_url

    prod_db = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(prod_db)
