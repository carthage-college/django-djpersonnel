"""
Django base settings for project.
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from datetime import datetime
from collections import namedtuple

# Debug
DEBUG = True
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
#USE_TZ = False
USE_TZ = True
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'
SERVER_URL = ''
API_URL = '{}/{}'.format(SERVER_URL, 'api')
LIVEWHALE_API_URL = 'https://{}'.format(SERVER_URL)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = BASE_DIR
ADMIN_MEDIA_PREFIX = '/static/admin/'
ROOT_URL = '/apps/personnel/'
MEDIA_ROOT = '{}/assets/'.format(ROOT_DIR)
#MEDIA_URL = '{}assets/'.format(STATIC_URL)
MEDIA_URL = '/media/djpersonnel/'
STATIC_ROOT = '{}/static/'.format(ROOT_DIR)
STATIC_URL = '/static/djpersonnel/'
UPLOADS_DIR = '{}files/'.format(MEDIA_ROOT)
UPLOADS_URL = '{}files/'.format(MEDIA_URL)
ROOT_URLCONF = 'djpersonnel.urls'
WSGI_APPLICATION = 'djpersonnel.wsgi.application'
FILE_UPLOAD_PERMISSIONS=0o644
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
# sqlserver connection string
MSSQL_EARL = ''
# informix connection string
INFORMIX_ODBC = ''
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
    #'bootstrap_admin',
    'bootstrap4',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'djpersonnel.core',
    'djpersonnel.transaction',
    'djpersonnel.requisition',
    # needed for template tags
    'djtools',
    'loginas',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
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
'''
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
'''
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
    'djauth.backends.LDAPBackend',
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
# security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
# bootstrap admin
BOOTSTRAP_ADMIN_SIDEBAR_MENU = True
# bootstrap forms
BOOTSTRAP4 = {
    'required_css_class': 'required',
}
# apps
HR_EMAIL=''
ACCOUNTING_EMAIL = ''
HR_GROUP='Human Resources'
STAFF_GROUP='carthageStaffStatus'
# approval level positions
TposStruct = namedtuple('TposStruct', 'id email')
DEANS_TPOS=(3374, 3375, 3376, 3561)
PROVOST_TPOS=2877
LEVEL2_TPOS=2760 #VPFA
LEVEL3_GROUP='Level 3'
TPOS_DEFAULT = {
    PROVOST_TPOS: TposStruct(id=0, email=''),
    LEVEL2_TPOS: TposStruct(id=0, email=''),
}
# tests
TEST_USER_USERNAME = ''
TEST_USER_PASSWORD = ''
TEST_USER_EMAIL = ''
TEST_USER_ID = 0
TEST_USER_FIRSTNAME = ''
TEST_USER_LASTNAME = ''
TEST_CREATED_AT_DATE = datetime(2018, 5, 1, 16, 20, 0)
TEST_LEVEL3_APPROVER_ID = 0
TEST_LEVEL2_APPROVER_ID = 0
TEST_LEVEl1_APPROVER_ID = 0
# logging
LOG_FILEPATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs/')
DEBUG_LOG_FILENAME = LOG_FILEPATH + 'debug.log'
INFO_LOG_FILENAME = LOG_FILEPATH + 'info.log'
ERROR_LOG_FILENAME = LOG_FILEPATH + 'error.log'
CUSTOM_LOG_FILENAME = LOG_FILEPATH + 'custom.log'
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
        'custom': {
            'format': '%(asctime)s: %(levelname)s: %(message)s',
            'datefmt' : '%m/%d/%Y %I:%M:%S %p'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'custom_logfile': {
            'level':'ERROR',
            'filters': ['require_debug_true'], # do not run error logger in production
            'class': 'logging.FileHandler',
            'filename': CUSTOM_LOG_FILENAME,
            'formatter': 'standard',
        },
        'info_logfile': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'backupCount': 10,
            'maxBytes': 50000,
            'filters': ['require_debug_false'], # run logger in production
            'filename': INFO_LOG_FILENAME,
            'formatter': 'standard',
        },
        'debug_logfile': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'], # do not run debug logger in production
            'class': 'logging.FileHandler',
            'filename': DEBUG_LOG_FILENAME,
            'formatter': 'verbose'
        },
        'error_logfile': {
            'level': 'ERROR',
            'filters': ['require_debug_true'], # do not run error logger in production
            'class': 'logging.FileHandler',
            'filename': ERROR_LOG_FILENAME,
            'formatter': 'verbose'
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
        'djpersonnel': {
            'handlers':['debug_logfile'],
            'propagate': True,
            'level':'DEBUG',
        },
        'djpersonnel.core': {
            'handlers':['debug_logfile'],
            'propagate': True,
            'level':'DEBUG',
        },
        'provisioning_logger': {
            'handlers': ['error_logfile'],
            'level': 'ERROR'
         },
        'error_logger': {
            'handlers': ['error_logfile'],
            'level': 'ERROR'
         },
        'info_logger': {
            'handlers': ['info_logfile'],
            'level': 'INFO'
        },
        'debug_logger': {
            'handlers':['debug_logfile'],
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
