import os
import sys

import django
import environ
import sentry_sdk
from django.utils.encoding import force_str
from sentry_sdk.integrations.django import DjangoIntegration

django.utils.encoding.force_text = force_str

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# False if not in os.environ because of casting above
DEBUG = env("DEBUG")
IS_PROD = env('IS_PROD', default=False)

SECRET_KEY = env("SECRET_KEY", default="replace_me")

WEB_APP_BASE_URL = env("WEB_APP_BASE_URL", default="http://localhost:3000")

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = [
    WEB_APP_BASE_URL,
    "http://localhost",
    "http://127.0.0.1",
    "http://0.0.0.0",
    'https://kplc-outages-be.fly.dev',
    'http://kplc-outages-be.fly.dev',
    'https://*.edge.ke',
    'https://kplc-outages-staging.fly.dev',
    'https://kplc-outages.fly.dev'
]
USE_X_FORWARDED_HOST = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # installed deps
    "django.contrib.sites",
    "graphene_django",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "allauth.socialaccount.providers.twitter",
    # 'allauth.socialaccount.providers.facebook',
    "anymail",
    "drf_yasg",
    # code
    "users",
    "outages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTH_USER_MODEL = "users.User"
ROOT_URLCONF = "kplc_outages.urls"
CORS_ORIGIN_ALLOW_ALL = True
SITE_ID = 1

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "common.pagination.PageNumberWithSizePagination",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ],
}

GRAPHENE = {"SCHEMA": "kplc_outages.schema.schema"}
## ========== auth stuff =========

# dj_rest_auth
REST_USE_JWT = True
JWT_AUTH_COOKIE = "auth-token"
JWT_AUTH_REFRESH_COOKIE = "refresh-token"
JWT_AUTH_SECURE = IS_PROD
OLD_PASSWORD_FIELD_ENABLED = True

# django allauth
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "offline",
        },
    }
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "kplc_outages.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": env.db(default="postgres://postgres:postgres@db:5432/kplc_outages")
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ============ email stuff ==============

if IS_PROD:
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = "noreply@kplc.edge.ke"

ANYMAIL = {
    "MAILGUN_API_KEY": env("MAILGUN_API_KEY", default="replace_me"),
    "MAILGUN_API_URL": "https://api.eu.mailgun.net/v3",
}

# logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': u"[{%(pathname)s:%(lineno)d} - %(levelname)-0s] (%(filename)s:%(lineno)d %(funcName)s) %(message)s",
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': sys.stdout,
        }
    },
    'loggers': {
        # root logger
        'backend': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        }
    }
}

# Sentry stuff
if IS_PROD:
    sentry_sdk.init(
        dsn=env("SENTRY_DSN", default='replace_me'),
        integrations=[
            DjangoIntegration(),
        ],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
