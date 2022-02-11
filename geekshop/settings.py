"""
Django settings for geekshop project.

Generated by 'django-admin startproject' using Django 3.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os.path

import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# env variables
path_env = Path(BASE_DIR, 'env.json')
with open(file=path_env, encoding='utf-8') as f:
    env = json.load(f)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p%cg)vrj=s1qy_doiap05z7(*n1k7jp1@u)r58xmvtf1!3%(i+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost:25',
    'localhost:8000',
    'localhost',
    'http://localhost:8000',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainapp.apps.MainappConfig',
    'authnapp.apps.AuthnappConfig',
    'basketapp.apps.BasketappConfig',
    'adminapp.apps.AdminappConfig',
    'social_django.apps.PythonSocialAuthConfig',
    'ordersapp.apps.OrdersappConfig',
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

ROOT_URLCONF = 'geekshop.urls'

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
                'mainapp.context_processors.basket',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'django.template.context_processors.media',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.vk.VKOAuth2',
)

WSGI_APPLICATION = 'geekshop.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': Path(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

if not DEBUG:
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
else:
    AUTH_PASSWORD_VALIDATORS = []

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    Path(BASE_DIR, 'static'),
)

# STATIC_ROOT = Path(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = Path(BASE_DIR, 'media')

# Auth model
AUTH_USER_MODEL = 'authnapp.ShopUser'

# Login url
# Set login path:
# https://docs.djangoproject.com/en/2.2/ref/settings/#login-url

LOGIN_URL = 'auth:login'

# mail
DOMAIN_NAME = 'http://localhost:8000'

# Read about sending email:
#   https://docs.djangoproject.com/en/3.2/topics/email/

EMAIL_HOST = 'localhost'
EMAIL_PORT = '25'

EMAIL_USE_SSL = False
# If server support TLS:
# EMAIL_USE_TLS = True

# EMAIL_HOST_USER = 'django@geekshop.local'
# EMAIL_HOST_PASSWORD = 'geekshop'
# For debugging: python -m smtpd -n -c DebuggingServer localhost:25
EMAIL_HOST_USER = None
EMAIL_HOST_PASSWORD = None

# Email as files
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'temp/email-messages/'

BASE_URL = 'http://localhost:8000'

# Auth to GitHub
# SOCIAL_AUTH_GITHUB_KEY = env.get('github_client_id')
SOCIAL_AUTH_GITHUB_KEY = env['github_client_id']
SOCIAL_AUTH_GITHUB_SECRET = env.get('github_client_secret')

# Auth to VK
SOCIAL_AUTH_VK_OAUTH2_KEY = env.get('vk_client_id')
SOCIAL_AUTH_VK_OAUTH2_SECRET = env.get('vk_client_id')

SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Django Debug Toolbar --->
if DEBUG:
    INSTALLED_APPS.extend([
        "debug_toolbar",
        "template_profiler_panel",
        "django_extensions",
    ])

if DEBUG:
    MIDDLEWARE.extend([
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ])

# Debgu tool bar settings
if DEBUG:
    def show_toolbar(request):
        return True


    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }

    DEBUG_TOOLBAR_PANELS = [
        # "ddt_request_history.panels.request_history.RequestHistoryPanel",
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
        "template_profiler_panel.panels.template.TemplateProfilerPanel",
    ]
# <--- Django Debug Toolbar
