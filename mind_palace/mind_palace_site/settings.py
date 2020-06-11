"""
Django settings for mind_palace project.

Environment variables to set:

MIND_PALACE_STATIC_DIR      -- path to dir where static files will be hosted / used by collectstatic
MIND_PALACE_SQLITE          -- path to sqlite database
MIND_PALACE_LOGFILE         -- path to logfile to use
MIND_PALACE_DEBUG           -- whether to run mind palace in debug mode
MIND_PALACE_URL_PREFIX      -- URL prefix if hosting under a URL, for example "foobar/"
MIND_PALACE_SECRET_KEY      -- secret key
MIND_PALACE_HOSTS           -- allowed hosts, "*" by default
MIND_PALACE_TIME_ZONE       -- local time zone to use for the server, e.g. "Europe/London"
"""

import os

# Prefix every URL with a path. Good for multihosting or obfuscation.
# For example: "foobar/"
MIND_PALACE_URL_PREFIX = os.environ.get('MIND_PALACE_URL_PREFIX', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if os.environ.get('MIND_PALACE_DEBUG') == 'True':
    DEBUG = True
print(f'Mind Palace Settings: DEBUG={DEBUG}')

# Basics

ROOT_URLCONF = 'mind_palace.mind_palace_site.urls'
WSGI_APPLICATION = 'mind_palace.mind_palace_site.wsgi.application'

# Security

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('MIND_PALACE_SECRET_KEY', '^olk9q!kx^lcz!ql-x@0h8xx3%6c+w!cp1e*6)4sc&+lrd!r(9')
ALLOWED_HOSTS = os.environ.get('MIND_PALACE_HOSTS', '*').split(',')
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
# Secure cookies ensure HTTPS is used
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
if DEBUG is False:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

# Applications

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'mind_palace.mind_palace_main'
]

# Middlewares

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Templates

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
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'environment': 'mind_palace.mind_palace_main.utils.jinja_environment',
        },
    },
]

# Static files

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATIC_ROOT = os.environ['MIND_PALACE_STATIC_DIR']
STATIC_URL = '/' + MIND_PALACE_URL_PREFIX + 'static/'

# Databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ['MIND_PALACE_SQLITE']
    }
}

# Authentication

LOGIN_URL = f'/{MIND_PALACE_URL_PREFIX}login/'
LOGIN_REDIRECT_URL = f'/{MIND_PALACE_URL_PREFIX}'
LOGOUT_REDIRECT_URL = f'/{MIND_PALACE_URL_PREFIX}'
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

# Languages and timezones

LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.environ.get('MIND_PALACE_TIME_ZONE', 'UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True
MORNING_HOURS = 3
EVENING_HOURS = 15

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.environ['MIND_PALACE_LOGFILE'],
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'logfile']
    },
}

# REST Framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
