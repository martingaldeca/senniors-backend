import os
import sys
from datetime import timedelta
from os.path import abspath
from os.path import dirname
from os.path import join

from corsheaders.defaults import default_headers
from corsheaders.defaults import default_methods
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from IPython.terminal.interactiveshell import TerminalInteractiveShell
from pytz import timezone as global_timezone

from backend.prompt import BackendPrompt

env = os.environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROUTER_IP = env.get('ROUTER_IP')
SECRET_KEY = env.get('DJANGO_SECRET_KEY')
DEBUG = env.get('DEBUG', 'True') == 'True'
DEBUG_SQL = env.get('DEBUG_SQL', 'True') == 'True'
PRODUCTION = env.get('PRODUCTION', 'True') == 'True'
ENVIRONMENT = env.get('ENVIRONMENT', 'unknown')
WSGI_APPLICATION = 'backend.wsgi.application'
ROOT_URLCONF = 'backend.urls'
ACCESS_TOKEN_LIFETIME_MINUTES = int(env.get('ACCESS_TOKEN_LIFETIME_MINUTES', 60))
REFRESH_TOKEN_LIFETIME_DAYS = int(env.get('REFRESH_TOKEN_LIFETIME_DAYS', 7))
SLIDING_TOKEN_LIFETIME_MINUTES = int(env.get('SLIDING_TOKEN_LIFETIME_MINUTES', 60))
SLIDING_TOKEN_REFRESH_LIFETIME_DAYS = int(env.get('SLIDING_TOKEN_REFRESH_LIFETIME_DAYS', 7))

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'Europe/Madrid'
timezone.activate('Europe/Madrid')
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/src/static/'
STATIC_ROOT = '/src/static/'
STATICFILES_DIRS = ['/src/backend/static']
MEDIA_URL = '/src/media/'
MEDIA_ROOT = '/src/media/'
MEDIAFILES_DIRS = ['/src/backend/media']

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

INTERNAL_APPS = [
    'core'
]

EXTERNAL_LIBRARIES = [
    'simple_history',
    'debug_toolbar',
    'django_extensions',
    'rest_framework',
    'corsheaders',
    'waffle',
    'axes',
    'drf_api_logger',
    'rest_framework_simplejwt',
    'drf_spectacular',
]

BASE_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
INSTALLED_APPS = BASE_APPS + INTERNAL_APPS + EXTERNAL_LIBRARIES

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',

    'waffle.middleware.WaffleMiddleware',
    'drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware',
    'axes.middleware.AxesMiddleware',  # Should be the last for axes to render lockout messages
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'axes.backends.AxesBackend',  # AxesBackend should be ... before something ? XD
    'rest_framework.authentication.TokenAuthentication',
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': int(env.get('PASSWORD_MIN_LENGTH', 7)),
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'core.User'

X_FRAME_OPTIONS = 'SAMEORIGIN'

LOCALE_PATHS = ('locale',)

PROJECT_ROOT = dirname(dirname(abspath(__file__)))
SITE_ROOT = dirname(PROJECT_ROOT)
SITE_NAME = 'Senniors backend'
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, join(SITE_ROOT, 'apps'))

global_timezone('Europe/Madrid')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'PAGE_SIZE': 25
}

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

DRF_API_LOGGER_DATABASE = True
DRF_API_LOGGER_SIGNAL = True
DRF_API_LOGGER_PATH_TYPE = 'ABSOLUTE'

REDIS_HOST = env.get('REDIS_HOST')
REDIS_PORT = env.get('REDIS_PORT')
REDIS_DB = int(env.get('REDIS_DB', default=0))

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
}

env = os.environ
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.get('POSTGRES_DB'),
        'USER': env.get('POSTGRES_USER'),
        'PASSWORD': env.get('POSTGRES_PASSWORD'),
        'HOST': env.get('POSTGRES_HOST'),
        'PORT': '',
    }
}

JET_SIDE_MENU_ITEMS = [
    {
        'label': _('Users'),
        'app_label': 'core',
        'items': [
            {'name': 'user'},
            {'name': 'clinichistory'},
        ]
    },
    {
        'label': _('Appointments'),
        'app_label': 'core',
        'items': [
            {'name': 'appointment'},
        ]
    },
]

JET_CHANGE_FORM_SIBLING_LINKS = False
JET_SIDE_MENU_COMPACT = True

JET_THEMES = [
    {
        'theme': 'default',  # theme folder name
        'color': '#47bac1',  # color of the theme's button in user menu
        'title': 'Default'  # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]

log_level_for_log_files = 'INFO'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s (%(name)s) %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # 'file_main': {
        #     'level': log_level_for_log_files,
        #     'class': 'logging.handlers.WatchedFileHandler',
        #     'filename': f'{os.environ.get("LOGGING_ROOT_DIR")}/{os.environ.get("PROJECT_NAME")}.log',
        #     'formatter': 'simple'
        # },
    },
    'loggers': {
        '': {
            'handlers': ['console',],
            'level': 'INFO',
        },
        'django': {
            'handlers': ['console', ],
            'level': 'INFO',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', ],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
    }
}

TerminalInteractiveShell.prompts_class = BackendPrompt
TerminalInteractiveShell.highlighting_style_overrides = BackendPrompt.get_style()

IPYTHON_ARGUMENTS = ['--ext', 'autoreload', ]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=REFRESH_TOKEN_LIFETIME_DAYS),
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=SLIDING_TOKEN_LIFETIME_MINUTES),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=SLIDING_TOKEN_REFRESH_LIFETIME_DAYS),
}

ALLOWED_HOSTS = [
    'localhost', '0.0.0.0', '127.0.0.1',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost",
    "http://0.0.0.0",
    "http://localhost:8080",
    "http://0.0.0.0:8080",
    "http://127.0.0.1:8080",
]

WAFFLE_CREATE_MISSING_SWITCHES = True

# Some Axes config
AXES_ENABLED = True
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = timedelta(minutes=30)  # Period of inactivity to clear failed attempts
AXES_RESET_ON_SUCCESS = True  # a successful login will reset the number of failed logins

# Sentry configuration
SHELL_PLUS = "ipython"
if DEBUG_SQL:
    SHELL_PLUS_PRINT_SQL = True
    SHELL_PLUS_PRINT_SQL_TRUNCATE = None
SHELL_PLUS_IMPORTS = []

if not PRODUCTION:
    SHELL_PLUS_IMPORTS.append(
        'from core.factories import *'
    )

if PRODUCTION:
    INSTALLED_APPS += [
        'storages'
    ]
    AWS_DEFAULT_ACL = None

    AWS_QUERYSTRING_AUTH = False
    AWS_S3_REGION_NAME = env.get('AWS_S3_REGION_NAME', '')
    AWS_ACCESS_KEY_ID = env.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = env.get('AWS_SECRET_ACCESS_KEY', '')

    # Static files
    AWS_STORAGE_BUCKET_NAME = env.get('AWS_STORAGE_BUCKET_NAME', '')
    STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/'
    STATICFILES_STORAGE = 'backend.storage.storage_backends.StaticStorage'
    STATIC_ROOT = 'src/static/'

    # Media files
    AWS_STORAGE_MEDIA_BUCKET_NAME = env.get('AWS_STORAGE_MEDIA_BUCKET_NAME', '')
    MEDIA_URL = f'https://{AWS_STORAGE_MEDIA_BUCKET_NAME}.s3.amazonaws.com/'
    DEFAULT_FILE_STORAGE = 'backend.storage.storage_backends.MediaStorage'
    MEDIA_ROOT = 'src/media/'

    ALLOWED_HOSTS += [
        f'{AWS_STORAGE_MEDIA_BUCKET_NAME}.s3.amazonaws.com',
        f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    ]
    CORS_ALLOWED_ORIGINS += [
        f'https://{AWS_STORAGE_MEDIA_BUCKET_NAME}.s3.amazonaws.com',
        f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com',
    ]

SPECTACULAR_SETTINGS = {
    'TITLE': 'Senniors backend',
    'DESCRIPTION': 'Backend for the senniors code test',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}