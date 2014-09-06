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
)

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
    'django_forms_bootstrap',
    'haystack',
    'taggit',
    'south',
    'social_auth',
    'jobs',
]

# Auth stuff
AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.contrib.bitbucket.BitbucketBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
    'social_auth.backends.OpenIDBackend',
    'social_auth.backends.browserid.BrowserIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY', '')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET', '')
BITBUCKET_CONSUMER_KEY = os.environ.get('BITBUCKET_CONSUMER_KEY', '')
BITBUCKET_CONSUMER_SECRET = os.environ.get('BITBUCKET_CONSUMER_SECRET', '')
GITHUB_APP_ID = os.environ.get('GITHUB_APP_ID', '')
GITHUB_API_SECRET = os.environ.get('GITHUB_API_SECRET', '')
FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID', '')
FACEBOOK_API_SECRET = os.environ.get('FACEBOOK_API_SECRET', '')
LINKEDIN_CONSUMER_KEY = os.environ.get('LINKEDIN_CONSUMER_KEY', '')
LINKEDIN_CONSUMER_SECRET = os.environ.get('LINKEDIN_CONSUMER_SECRET', '')

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_COMPLETE_URL_NAME = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

# Mailhide
MAILHIDE_PUBLIC_KEY = os.environ.get('MAILHIDE_PUBLIC_KEY', '')
MAILHIDE_PRIVATE_KEY = os.environ.get('MAILHIDE_PRIVATE_KEY', '')

# Testing
TEST_RUNNER = 'discover_runner.DiscoverRunner'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'requests': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'jobs',
    },
}
HAYSTACK_DOCUMENT_FIELD = '_all'
