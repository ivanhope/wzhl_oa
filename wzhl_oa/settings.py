# Django settings for wzhl_oa project.
# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wzhl',
	    'USER': 'admin',
	    'PASSWORD': '!@#rp1qaz@WSX',
	    'HOST': '127.0.0.1',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, "static"),
    '/static_admin/',
    '/media/'
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#ioag^zjg!+wq^=x-jum(qz*)*&amp;*h&amp;v@_#@_ks%7l3=dyzqu_t'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'wzhl_oa.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wzhl_oa.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    BASE_DIR+'/templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    # 'debugtools',
    'user_manage',
    'order_form',
    'vacation',
    'work_out',
    'assets',
    'KPI',
    'personal_information',
    'business_trip',
    'contract',
    'seal',
    'repay',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
     'version': 1,
     'disable_existing_loggers': True,
     'formatters': {
         'simple': {
             'format': '[%(asctime)s] %(levelname)s : %(message)s'
         },
         'verbose': {
             'format': '[%(asctime)s] %(levelname)s %(module)s %(process)d %(thread)d : %(message)s'
         },
     },
     'handlers': {
         'null': {
             'level': 'DEBUG',
             'class': 'django.utils.log.NullHandler',
         },
         'console': {
             'level': 'INFO',
             'class': 'logging.StreamHandler',
             'formatter': 'simple',
         },
         'file': {
             'level': 'INFO',
             'class': 'logging.FileHandler',
             'formatter': 'simple',
             'filename': BASE_DIR+'/logs/sys.log',
             'mode': 'a',
         },
     },
     'loggers': {
         'django': {
             'handlers': ['file', 'console'],
             'level':'INFO',
             'propagate': True,
         },
     },
 }

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
   # 'django.core.context_processors.debug',
   # 'django.core.context_processors.i18n',
   # 'django.core.context_processors.media',
   # 'tools.my_template_context_processors.request_filter',
)

#DATAFILE_MAXSIZE = 1024000000
#DATAFILE_TMP_MAXSIZE = 1024000000
#FILE_UPLOAD_MAX_MEMORY_SIZE =  1024000000
#FILE_UPLOAD_TEMP_DIR = 'tmp'

#??????crontab
#??????????????????
#0 5 25 * * /usr/bin/python /usr/share/nginx/wzhl_oa/libs/refresh_script.py assets_refresh
#????????????
#0 10 * * * /usr/bin/python /usr/share/nginx/wzhl_oa/libs/refresh_script.py vacation_refresh


#custom
HR = {'name':'?????????','email':'liuyaling@xiaoquan.com'}
administration = {'name':'?????????','email':'liuyaling@xiaoquan.com'}
BossName = ['??????','??????']
department_BossName = ['??????','??????','??????','?????????','?????????','?????????','??????','??????']

description = ['?????????','?????????','?????????','?????????','?????????','?????????','ipad','imac','?????????','?????????','?????????','??????']
model = ['?????????DELL???9020MT???????????????','???????????? ???????????????','?????????DELL???U2414H ???????????????','?????????DELL???R620 ?????????',
         '????????????????????????','???????????????','????????? SK-860?????????','?????????hp???MFP M277dw ???????????????','??????HP M427dw ???????????????',
         'iPad???????????? 16G WiFi?????????','iPad???????????? 16G WiFi?????????','27 ???????????? Retina 5K ???????????? iMac',
         '21.5 ?????? iMac ??????????????? 2.9GHZ','21.5 ?????? iMac ??????????????? 2.7GHZ',
         '?????????ThinkPad?????????????????????E450???????????????','??????????????????????????????&UPS???','?????????DELL???R730 ?????????',
         '?????????DELL???R230 ?????????','??????S6720S-26Q-EI-24S????????????&??????','??????USG6370????????????&??????']
category = {'????????????':[36,'HUBFAA'], '??????':[48,'HUBFAB'], '????????????':[60,'HUBFAC']}
department = ['?????????','?????????','?????????','?????????']
