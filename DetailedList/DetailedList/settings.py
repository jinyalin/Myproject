"""
Django settings for DetailedList project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import socket
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4h5z%-*il!l6yz@k78t1ezlrbwqe-k#$nvl$&a#6**!e3%+37y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'SmsSp',
    'SmsCluster',
    'SmsGate',
    'Login',
    'ShareMethod',
    'LogAnalysis',
    'CommandQuery',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'DetailedList.urls'

WSGI_APPLICATION = 'DetailedList.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'monitor_server',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '192.168.120.12',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'
FILE_CHARSET = 'utf-8'
DEFAULT_CHARSET = 'utf-8'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL='/media/'

STATIC_ROOT = 'static'

if socket.gethostname() == 'hskj-backup250':
    STATIC_PATH='/hskj/web/apache/htdocs/DetailedList/static'

    TEMPLATE_DIRS = (
                 '/hskj/web/apache/htdocs/DetailedList/ShareMethod/templates',
                 )

else:
    STATIC_PATH='E:\workspace\DetailedList\static'

    TEMPLATE_DIRS = (
                 'E:\workspace\DetailedList\ShareMethod\templates',
                 )
