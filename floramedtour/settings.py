from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv
import dj_database_url
from .logging_setup import LOGGING

DEVELOPMENT_MODE = True
VERSION = "2.0.0"

load_dotenv()
# ROOT_DIR = environ.Path(__file__) - 2
parent_dir = os.path.dirname(os.path.abspath(__file__))

# env = environ.Env()
# environ.Env.read_env(str(parent_dir.path('.env')))

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# SESSION_COOKIE_DOMAIN = 'your-domain.com'
# SESSION_COOKIE_PATH = '/your-path'
# CSRF_COOKIE_DOMAIN = 'your-domain.com'
# CSRF_COOKIE_PATH = '/your-path'

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Application definition

INSTALLED_APPS = [
    'administration',
    'food',
    'nursing',
    'shopping',
    'tourism',
    'accommodation',
    'transportation',
    'treatment',
    'common',
    'communication',
    'financialhub',
    # 'debug_toolbar',
    # 'logtailer',
    'django_extensions',
    'rest_framework',
    'rest_framework_simplejwt',
    'sslserver',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    # 'django_hosts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_user_agents',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'common.middleware.JWTAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

ROOT_URLCONF = 'floramedtour.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'common.context_processors.user_context.user_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'floramedtour.wsgi.application'

# CELERY_BROKER_URL = 'redis://localhost:6379/0'  # اگر Redis را به عنوان بروکر انتخاب کرده‌اید
# # یا
# CELERY_BROKER_URL = 'pyamqp://guest:guest@localhost//'

# # برای نتایج
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # اگر Redis را به عنوان بروکر انتخاب کرده‌اید
# # یا
# CELERY_RESULT_BACKEND = 'rpc://'

# DATABASES = {
#     'default': os.getenv('DATABASE_URL')
# }

DATABASES = {
    'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
}

DEFAULT_CHARSET = 'utf-8'

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

AUTH_USER_MODEL = "common.User"

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

GEOIP_PATH = os.path.join(BASE_DIR, 'geoip_data')

STATIC_ROOT = BASE_DIR / 'productionfiles'

STATIC_URL = 'static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = []

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

GRAPH_MODELS ={
'all_applications': True,
'graph_models': True,
}

# ROOT_HOSTCONF = 'project.hosts'  # اسم فایل hosts.py شما
# DEFAULT_HOST = 'www'

PRIVATE_KEY = os.getenv('PRIVATE_KEY').replace('\\n', '\n')
PUBLIC_KEY = os.getenv('PUBLIC_KEY').replace('\\n', '\n')

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=3),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'ALGORITHM': 'RS256',
    'SIGNING_KEY': PRIVATE_KEY,
    'VERIFYING_KEY': PUBLIC_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'AUTH_COOKIE_CLASSES': ('rest_framework_simplejwt.tokens.SlidingToken',),
}

# Django Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'django.contrib.auth.backends.ModelBackend',  # For session authentication
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
    # ... (any other DRF settings you have)
}

APPEND_SLASH = True

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # '5.39.60.120'
]

CORS_ALLOWED_ORIGINS = [
    "https://127.0.0.1:8000",
    "https://floramedtour.com",
]



# Register the function to be called on exit

# if 'debug_toolbar' in INSTALLED_APPS:
#     INSTALLED_APPS.remove('debug_toolbar')
# if 'debug_toolbar.middleware.DebugToolbarMiddleware' in MIDDLEWARE:
#     MIDDLEWARE.remove('debug_toolbar.middleware.DebugToolbarMiddleware')

# if 'debug_toolbar' not in INSTALLED_APPS:
#     INSTALLED_APPS.append('debug_toolbar')
# if 'debug_toolbar.middleware.DebugToolbarMiddleware' not in MIDDLEWARE:
#     MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

"""
Version:
2.0.0: revived after disaster entire root deletion with my wife's moral, psychological and emotional support.
"""