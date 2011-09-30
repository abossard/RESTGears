# Initialize App Engine and import the default settings (DB backend, etc.).
# If you want to use a different backend you have to remove all occurences
# of "djangoappengine" from this file.
from djangoappengine.settings_base import *

import os
project_dir = os.path.dirname(globals()["__file__"])

# Activate django-dbindexer for the default database
DATABASES['native'] = DATABASES['default']
DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
AUTOLOAD_SITECONF = 'indexes'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ENABLE_PROFILER = False

EXTRA_PROFILE_OUTPUT = ()
SORT_PROFILE_RESULTS_BY = ('cumulative','calls','time')
MAX_PROFILE_RESULTS = 25
ADMINS = (
     #('Your name', 'your_email@example.com'),
)

TIME_ZONE = 'Europe/Zurich'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

#from base.sites import SiteIDHook
#SITE_ID = 1

USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False


SECRET_KEY = '=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'

INSTALLED_APPS = (
#    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    #'django.contrib.sites',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',

    'djangorestframework',
    'dbindexer',
    
    'base',

    #'stats',
    'publisher',
    'gallery',

    'djangotoolbox',
    'permission_backend_nonrel',
    'account',
    'autoload',


    'filetransfers',

    'debug_toolbar',
    # djangoappengine should come last, so it can override a few manage.py commands
    'djangoappengine',
)



PREPARE_UPLOAD_BACKEND = 'djangoappengine.storage.prepare_upload'
SERVE_FILE_BACKEND = 'djangoappengine.storage.serve_file'
PUBLIC_DOWNLOAD_URL_BACKEND = 'filetransfers.backends.default.public_download_url'

AUTH_PROFILE_MODULE = 'account.UserProfile'

AUTHENTICATION_BACKENDS = (
    'permission_backend_nonrel.backends.NonrelPermissionBackend',
    'account.backends.DeviceAuthTokenBackend',
    #'django.contrib.auth.backends.ModelBackend',
    )
MIDDLEWARE_CLASSES = (
    # This loads the index definitions, so it has to come first
    'django.middleware.cache.UpdateCacheMiddleware',   
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'autoload.middleware.AutoloadMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'base.middleware.BlobRedirectFixMiddleware',
    
    'django.middleware.cache.FetchFromCacheMiddleware',

   # 'debug_toolbar.middleware.DebugToolbarMiddleware',
)
INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    #'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    #'debug_toolbar.panels.cache.CacheDebugPanel',
)
DEBUG_TOOLBAR_CONFIG ={
                       'INTERCEPT_REDIRECTS' : False
                       }


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
)

# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

ADMIN_MEDIA_PREFIX = '/media/admin/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#MEDIA_ROOT = ''
MEDIA_ROOT = os.path.join(project_dir,'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'


TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
    )

ROOT_URLCONF = 'urls'


DBINDEXER_BACKENDS = (
    'dbindexer.backends.BaseResolver',
    'dbindexer.backends.InMemoryJOINResolver',
    'dbindexer.backends.FKNullFix',
)


#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '',
#        'TIMEOUT': 0,
#    }
#}
#USE_ETAGS = True
#CACHE_MIDDLEWARE_ALIAS = 'middleware-cache'
CACHE_MIDDLEWARE_SECONDS = 30
#CACHE_MIDDLEWARE_KEY_PREFIX = 'powerfood2011'
