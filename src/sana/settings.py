"""Django settings for Sana project. 

This file contains the application configuration variables is available with
all default values as: ::

    settings.py.tmpl

and should be renamed to settings.py prior to filling in local values. Once 
updated, enter the following from the mds installation directory::
    
    $> ./manage.py syncdb
    
This will require root privileges. 
    
:Authors: Sana Dev team
:Version: 2.0
:Requires: Django 1.3
"""

DEBUG = True
''' Global debug level. Should be set to False in production environments. '''

TEMPLATE_DEBUG = DEBUG
''' Template debug level. Should be set to False in production environments. '''

ADMINS = (
    ('admin', 'admin@localhost.com'),
)
''' Tuple of admin names and email addresses. '''

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'NAME': '/opt/sana/sqlite.db',
        'ENGINE': 'django.db.backends.sqlite3',
        'USER': '',
        'PASSWORD': ''
    },
}
""" Database configuration:
    NAME: 'app_label' or path to database file if using sqlite3.
    ENGINE: 'django.db.backends' + one of:
            'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3', 'oracle'.
    USER: Not used with sqlite3.
    PASSWORD: Not used with sqlite3.
    HOST: Set to empty string for localhost. Not used with sqlite3.
    PORT: Set to empty string for default. Not used with sqlite3.        
"""


TIME_ZONE = 'America/Chicago'
"""Local time zone for this installation. Choices can be found here:

    http://en.wikipedia.org/wiki/List_of_tz_zones_by_name

although not all choices may be available on all operating systems.
If running in a Windows environment this must be set to the same as your
system time zone.
"""

LANGUAGE_CODE = 'en-us'
"""Language code for this installation. All choices can be found here:

    http://www.i18nguy.com/unicode/language-identifiers.html
"""

SITE_ID = 1
"""Don't touch this unless you know what you are doing."""


USE_I18N = True
"""If you set this to False, Django will make some optimizations so as not to 
load the internationalization machinery."""

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)
"""List of callables that know how to import templates from various sources."""

MEDIA_ROOT = '/home/ewinkler/git/sana.mds/src/sana/media/'
"""Absolute path to the directory that holds media. For a typical Sana 
deployment use: "/opt/sana/media/"
"""

MEDIA_URL = '/media/'
"""URL that handles the media served from MEDIA_ROOT. Make sure to use a
trailing slash if there is a path component (optional in other cases). For a 
typical Sana deployment use: "/mds/media/". """

STATIC_URL = "http://127.0.0.1:8000/static/"
STATIC_ROOT = '/opt/sana/static/'


ADMIN_MEDIA_PREFIX = '/media/'
"""URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
trailing slash. Examples: "http://foo.com/media/", "/media/".
"""

SECRET_KEY = 'b#%x46e0f=jx%_#-a9b5(4bvxlfz-obm*gs4iu3i6k!034j(mx'
"""Make this unique, and don't share it with anybody. Seriously."""


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'sana.api.contrib.middleware.LoggingMiddleware',
)
"""Don't touch this unless you know what you are doing."""

ROOT_URLCONF = 'sana.urls'
"""Don't touch this unless you know what you are doing."""

TEMPLATE_DIRS = (
        '/opt/sana/templates',
)
"""Put strings here, like "/home/html/django_templates" or 
"C:/www/django/templates". Always use forward slashes, even on Windows. Don't 
forget to use absolute paths, not relative paths.For a typical Sana 
deployment use: "/opt/sana/templates/"."""

INSTALLED_APPS = (        
    'sana.mrs',
    'sana.core',         
    'sana.mds',         
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.markup',
)
"""Don't touch this unless you know what you are doing."""

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

FIXTURE_DIRS = ()

try:
    from local_settings import *
except ImportError, exp:
    pass
