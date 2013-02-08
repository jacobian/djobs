from .base import *  # noqa

DEBUG = TEMPLATE_DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    import debug_toolbar  # noqa
except ImportError:
    pass
else:
    INSTALLED_APPS.append('debug_toolbar')
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE_CLASSES.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
