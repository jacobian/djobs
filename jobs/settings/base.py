import os
import postgresify
from unipath import FSPath as Path

# Basic setup
PROJECT_ROOT = Path(__file__).ancestor(2)
DEBUG = TEMPLATE_DEBUG = False
ROOT_URLCONF = 'jobs.urls'
SECRET_KEY = os.environ['SECRET_KEY']
SITE_ID = 1
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = True

# Databases
DATABASES = postgresify.postgresify()

# Media, assets, etc.
PROJECT_ROOT.child('media')
MEDIA_URL = '/media/'
STATIC_ROOT = PROJECT_ROOT.child('static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [PROJECT_ROOT.child('assets')]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Compressor
COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = ['compressor.filters.template.TemplateFilter']
COMPRESS_JS_FILTERS = ['compressor.filters.template.TemplateFilter']

# Templates
TEMPLATE_DIRS = [PROJECT_ROOT.child('templates')]

# Middleware
MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# Apps
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'compressor',
    'django_forms_bootstrap',
    'south',
    'jobs',
]

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'basic',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
