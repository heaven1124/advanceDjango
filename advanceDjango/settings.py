"""
Django settings for advanceDjango project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os.path
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jjoa7ylja0fy$*a$@jh=&7o9y%rgvpkfw*)#o^=v6#(5r!$&nx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'stockapp',
    'django_celery_results',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.check_login.CheckLoginMiddleware',
    'middleware.cache_page.CachePageMiddleware',
]

ROOT_URLCONF = 'advanceDjango.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'advanceDjango.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'advance1',
        'HOST': '10.0.0.48',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': '123456',
        'CHARSET': 'utf8'
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 配置Django的日志
LOGGING = {
    'version': 1.0,
    'formatters': {
        'base': {
            'format': '[%(asctime)s %(name)s] %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S'
        }
    },
    'handlers': {
        # 日志输出到控制台
        'out': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'base'
        },
        # 日志输出到文件
        'file': {
            'class': 'logging.FileHandler',
            'level': 'WARNING',
            'formatter': 'base',
            'filename': f'{BASE_DIR}/warn.log'
        },
        # 日志发送到指定邮箱
        # 'email': {
        #
        # }
    },
    'loggers': {
        'django': {
            'handlers': ['out', 'file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

# 配置缓存Cache
CACHES = {
    'file': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': f'{BASE_DIR}/mycache',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 500,
            'CULL_FREQUENCY': 3,
        }
    },
    'html': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    },
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://10.0.0.48:6379/10',
        'OPTIONS': {
            'PASSWORD': '123',
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 10,
            'SOCKET_TIMEOUT': 10,

            'MAX_ENTRIES': 500,
            'CULL_FREQUENCY': 3,
        }
    },
    # 'database': {
    #     'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
    #     'LOCATION': 'my_cache_table',
    #     'TIMEOUT': 60,
    #     'KEY_PREFIX': 'bbs',
    #     'VERSION': '1',
    #     'OPTIONS': {
    #         'MAX_ENTRIES': 500,
    #         'CULL_FREQUENCY': 3,
    #     }
    # }
}

# 配置session
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_COOKIE_NAME = 'SESSION_ID'
SESSION_COOKIE_PATH = '/'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 1209600 # 有效时间两周

# 配置celery
CELERY_IMPORTS = ('stockapp.tasks',)
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
