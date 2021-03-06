# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gh*j0e&=1q4&$z1&pemc)tk#)06#4u0o1qcw=0^9h)%(vpgda5'

# SECURITY WARNING: don't run with debug turned on in production!
import socket
#if socket.gethostname() == 'vm-ywcs03':
 #   DEBUG = TEMPLATE_DEBUG = False
#else:
DEBUG = TEMPLATE_DEBUG = True
    
ALLOWED_HOSTS = ['*']

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ShareMethod',
    'Login',
    'OpExcel',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     #'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'YysBill.urls'

WSGI_APPLICATION = 'YysBill.wsgi.application'


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
        'HOST': '',
        'PORT': '',
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

if socket.gethostname() == 'vm-ywcs03':
    STATIC_PATH='/hskj/web/apache/htdocs/YysBill/static'

    TEMPLATE_DIRS = (
                 '/hskj/web/apache/htdocs/YysBill/ShareMethod/templates',
                 )

else:
    STATIC_PATH='E:\workspace\YysBill\static'

    TEMPLATE_DIRS = (
                 'E:\workspace\YysBill\ShareMethod\templates',
                 )

