import os.path
import sys

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.join(PROJECT_PATH, 'apps'))


PUBLIC_PATH = os.path.join(PROJECT_PATH, 'public')

DEBUG = False
TEMPLATE_DEBUG = True

ADMINS = (
    # ('', ''),
)

LOCAL_DEVELOPMENT = False
MANAGERS = ADMINS

TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(PUBLIC_PATH, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PUBLIC_PATH, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'javascript_settings.middleware.JavaScriptUserConfig',
)

ROOT_URLCONF = 'uwc_first_stage.urls'

WSGI_APPLICATION = 'uwc_first_stage.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request'
)

FIXTURE_DIRS = (
    os.path.join(PROJECT_PATH, 'fixtures'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    # Plugins:
    'south',
    'javascript_settings',
    'ajax_select',
    'sorl.thumbnail',

    # Apps:
    'core',
    'providers',
    'products'
)

# define the lookup channels in use on the site
AJAX_LOOKUP_CHANNELS = {
    #   pass a dict with the model and the field to search against
    'parameters'  : {'model':'products.parameter', 'search_field':'name'},
    'parametervalues'  : {'model':'products.parametervalue', 'search_field':'value'}
}
AJAX_SELECT_INLINES = 'inline'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_PATH, 'logs', 'uwc_first_stage.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOCAL_INSTALLED_APPS = LOCAL_MIDDLEWARE_CLASSES = tuple()

try:
    from settings_local import *
except ImportError:
    print "LOCAL SETTINGS COULD NOT BE FOUND!"
else:
    INSTALLED_APPS += LOCAL_INSTALLED_APPS
    MIDDLEWARE_CLASSES += LOCAL_MIDDLEWARE_CLASSES
