
import environ
from hashids import Hashids
# from boto.s3.connection import (
#     S3Connection, ProtocolIndependentOrdinaryCallingFormat,
# )
# Build paths inside the project like this: BASE_DIR / 'subdir'.
ROOT_DIR = environ.Path(
    __file__) - 3
APPS_DIR = ROOT_DIR.path('src')
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
)
env.read_env(str(ROOT_DIR.path('.env')))

SECRET_KEY = env('SECRET_KEY')
HASHIDS = Hashids(salt=SECRET_KEY, min_length=8)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DJANGO_DEBUG')
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": env.get_value('DB_HOST', str, None),
        "NAME": env.get_value('DB_NAME', str, None),
        "USER": env.get_value('DB_USER', str, None),
        "PASSWORD": env.get_value('DB_PASSWORD', str, None),
        "PORT": env.get_value('DB_PORT', int, 4532)
    },
}

DATABASES['default']['CONN_MAX_AGE'] = 3600

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = "config.asgi.application"

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
]

THIRD_PARTY_APPS = [
    'ckeditor',
    'storages',
    'mptt',
    'prettyjson',
    'channels',
    ]

LOCAL_APPS = [
    'src.apps.conf',
    'src.apps.users',
    'src.apps.customers',
    'src.apps.companies',
    'src.apps.landing',
    'src.apps.events',
    'src.apps.tickets'
]

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + LOCAL_APPS

MIDDLEWARE = [
    'src.apps.core.middleware.MySubdomainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'src.apps.landing.context_processors.main_info',
            ],
        },
    },
]

AUTH_USER_MODEL = 'users.User'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = str(ROOT_DIR('staticfiles'))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]

STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'
MEDIA_URL = '/media/'
MEDIA_ROOT = str(APPS_DIR.path('media'))
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'  # noqa 501
DEFAULT_FILE_STORAGE = 'src.apps.core.storage.MediaStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = env.get_value(
    'EMAIL_BACKEND', str, "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = env.get_value('EMAIL_HOST', str, None)
EMAIL_HOST_USER = env.get_value('EMAIL_HOST_USER', str, None)
EMAIL_HOST_PASSWORD = env.get_value('EMAIL_HOST_PASSWORD', str, None)
DEFAULT_FROM_EMAIL = env.get_value('DEFAULT_FROM_EMAIL', str, None)
EMAIL_PORT = env.get_value('EMAIL_PORT', int, None)
EMAIL_USE_TLS = True

STATIC_VERSION = env.get_value('STATIC_VERSION', str, "001")
CHAT_URL = env.get_value('CHAT_URL', str, "")
RECAPTCHA_SITE_KEY = env.get_value('RECAPTCHA_SITE_KEY', str, "")
RECAPTCHA_SECRET_KEY = env.get_value('RECAPTCHA_SECRET_KEY', str, "")

AWS_STORAGE_BUCKET_NAME = env.get_value(
    'DJANGO_AWS_STORAGE_BUCKET_NAME', str, None)
AWS_ACCESS_KEY_ID = env.get_value('DJANGO_AWS_ACCESS_KEY_ID', str, None)
AWS_SECRET_ACCESS_KEY = env.get_value(
    'DJANGO_AWS_SECRET_ACCESS_KEY', str, None)
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME  # noqa 501
AWS_S3_SECURE_URLS = True
BUCKET_FOLDER_NAME = env.get_value('BUCKET_FOLDER_NAME', str, "")
AWS_DEFAULT_ACL = 'public-read'
REDIS_HOST = env.get_value('REDIS_HOST', str, "")

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, 6379)],
            "capacity": 2000,
            "expiry": 10,
        },
    },
}
