import configparser
import os
from datetime import timedelta
from pathlib import Path
import environ
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('jrw')

env = environ.Env()
env_file = str(ROOT_DIR.path('.env'))
env.read_env(env_file)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)
AUTH_USER_MODEL = 'user.User'
SITE_ID = env('SITE_ID')


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


CORS_ALLOWED_ORIGINS = env('CORS_ALLOWED_ORIGINS').split(",")

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = env('CORS_ORIGIN_WHITELIST').split(",")



LINK_SOCIAL_ACCOUNT_WITHOUT_LOGIN = True

SYS_ENV = env('SYS_ENV')

ROOT_URLCONF = 'jrw.urls'


# Application definition
DJANGO_APPS = (
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'corsheaders',
    'rest_framework',
    'ckeditor',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'channels'
)

LOCAL_APPS = (
    'user',
    'notification',
    'channel',
    'payment',
    'chat'
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]


ALLOWED_HOSTS = env('ALLOWED_HOST').split(",")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(ROOT_DIR.path('templates'))],
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

# WSGI_APPLICATION = 'jrw.wsgi.application'
ASGI_APPLICATION = "jrw.routing.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [('127.0.0.1', 6379)],
#         },
#     },
# }
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     },
# }

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_MIDDLEWARE_CLASSES': (
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
}

# simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=300),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=30),
}

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': 800,
    },
}

DATABASES = {'default': env.db('DATABASE_URL', default='postgresql://postgres:@localhost:5432/jrw'), }
# DATABASES = {
#     "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
# }

STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
    os.path.join(APPS_DIR, 'attachments')
)
STATIC_URL = 'static/'

MEDIA_ROOT = os.path.join(APPS_DIR, 'media')
MEDIA_URL = '/media/'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# DEFAULT_FILE_STORAGE = 'config.storage_backends.MediaStorage'

AWS_DEFAULT_ACL = None



#Email Config
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')


#Payment Config
if SYS_ENV=="development":
    STRIPE_SECRET_KEY = env('TEST_STRIPE_SECRET_KEY')
    STRIPE_PUBLISHABLE_KEY = env('TEST_STRIPE_PUBLISHABLE_KEY')
    TEST_CARD_TOKEN = env('TEST_CARD_TOKEN')
    STRIPE_BASE_URL = env('TEST_STRIPE_BASE_URL')
    STRIPE_PRODUCT_ID = env("TEST_PRODUCT_ID")
else:
    STRIPE_SECRET_KEY = env('LIVE_STRIPE_SECRET_KEY')
    STRIPE_PUBLISHABLE_KEY = env('LIVE_STRIPE_PUBLISHABLE_KEY')
    CARD_TOKEN = env('CARD_TOKEN')
    STRIPE_BASE_URL = env('LIVE_STRIPE_BASE_URL')
    STRIPE_PRODUCT_ID = env("PRODUCT_ID")
    


