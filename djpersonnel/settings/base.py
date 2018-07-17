"""
Django base settings for project.
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from djzbar.settings import INFORMIX_EARL_TEST as INFORMIX_EARL
from djzbar.settings import JX_EARL_PROD
from djzbar.settings import JX_EARL_TEST
from djzbar.settings import INFORMIX_ODBC

# Debug
DEBUG = False
INFORMIX_DEBUG = 'debug'
# include html5 form attributes in input fields
REQUIRED_ATTRIBUTE = True
ADMINS = (
    ('', ''),
)
MANAGERS = ADMINS
SECRET_KEY = ''
ALLOWED_HOSTS = []
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = False
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'
SERVER_URL = ''
API_URL = '{}/{}'.format(SERVER_URL, 'api')
LIVEWHALE_API_URL = 'https://{}'.format(SERVER_URL)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(__file__)
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATIC_URL = '/static/djpersonnel/'
ROOT_URL = '/apps/personnel/'
MEDIA_ROOT = '{}/assets/'.format(ROOT_DIR)
STATIC_ROOT = '{}/static/'.format(ROOT_DIR)
MEDIA_URL = '{}assets/'.format(STATIC_URL)
UPLOADS_DIR = '{}files/'.format(MEDIA_ROOT)
UPLOADS_URL = '{}files/'.format(MEDIA_URL)
ROOT_URLCONF = 'djpersonnel.urls'
WSGI_APPLICATION = 'djpersonnel.wsgi.application'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
DATABASES = {
    'default': {
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'django_djpersonnel',
        'ENGINE': 'django.db.backends.mysql',
        'USER': '',
        'PASSWORD': ''
    },
}
INSTALLED_APPS = [
    'bootstrap_admin',
    'bootstrap4',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'djpersonnel.dashboard',
    'djpersonnel.transaction',
    'djpersonnel.requisition',
    # needed for template tags
    'djtools',
]
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # the following should be uncommented unless you are
    # embedding your apps in iframes
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# template stuff
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            '/data2/django_templates/djkorra/',
            '/data2/django_templates/djbootmin/',
            '/data2/django_templates/djcher/',
            '/data2/django_templates/django-djskins/',
            '/data2/livewhale/includes/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug':DEBUG,
            'context_processors': [
                'djtools.context_processors.sitevars',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
            #'loaders': [
            #    # insert your TEMPLATE_LOADERS here
            #]
        },
    },
]
# caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        #'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        #'LOCATION': '127.0.0.1:11211',
        #'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        #'LOCATION': '/var/tmp/django_djpersonnel_cache',
        #'TIMEOUT': 60*20,
        #'KEY_PREFIX': 'djpersonnel_',
        #'OPTIONS': {
        #    'MAX_ENTRIES': 80000,
        #}
    }
}
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
# LDAP Constants
LDAP_SERVER = ''
LDAP_SERVER_PWM = ''
LDAP_PORT = ''
LDAP_PORT_PWM = ''
LDAP_PROTOCOL = ''
LDAP_PROTOCOL_PWM = ''
LDAP_BASE = ''
LDAP_USER = ''
LDAP_PASS = ''
LDAP_EMAIL_DOMAIN = ''
LDAP_OBJECT_CLASS = ''
LDAP_OBJECT_CLASS_LIST = []
LDAP_GROUPS = {}
LDAP_RETURN = []
LDAP_RETURN_PWM = []
LDAP_ID_ATTR = ''
LDAP_CHALLENGE_ATTR = ''
LDAP_AUTH_USER_PK = False
# auth backends
AUTHENTICATION_BACKENDS = (
    'djauth.ldapBackend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
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
LOGIN_URL = '{}accounts/login/'.format(ROOT_URL)
LOGOUT_URL = '{}accounts/logout/'.format(ROOT_URL)
LOGIN_REDIRECT_URL = ROOT_URL
USE_X_FORWARDED_HOST = True
#SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_DOMAIN='.carthage.edu'
SESSION_COOKIE_NAME ='django_djpersonnel_cookie'
SESSION_COOKIE_AGE = 86400
# SMTP settings
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_FAIL_SILENTLY = False
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
SERVER_MAIL=''
# bootstrap admin
BOOTSTRAP_ADMIN_SIDEBAR_MENU = True
# bootstrap forms
BOOTSTRAP4 = {
    'required_css_class': 'required',
}
# apps
PAF_EMAIL_LIST=[]
# tests
TEST_USERNAME = ''
TEST_PASSWORD = ''
TEST_EMAIL = ''
TEST_STUDENT_ID = 0
TEST_STUDENT_LASTNAME = ''

# logging
LOG_FILEPATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs/')
LOG_FILENAME = LOG_FILEPATH + 'debug.log'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt' : '%Y/%b/%d %H:%M:%S'
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt' : '%Y/%b/%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILENAME,
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'include_html': True,
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        '': {
            'handlers':['logfile'],
            'propagate': True,
            'level':'DEBUG',
        },
        'djpersonnel': {
            'handlers':['logfile'],
            'propagate': True,
            'level':'DEBUG',
        },
        'djpersonnel.core': {
            'handlers':['logfile'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
