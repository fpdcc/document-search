# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
import os
import socket

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a-very-secret-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Add dynamically generated Docker IP
# Don't do this in production!
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + '1' for ip in ips] + ['127.0.0.1']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'docsearch',
        'HOST': 'postgres',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': 'postgres'
    }
}

# Caching

CACHE_KEY = 'some key'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Static files

MEDIA_ROOT = '/media/'

# Haystack search
# https://django-haystack.readthedocs.io/en/master/tutorial.html

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://solr:8983/solr/document-search',
        'ADMIN_URL': 'http://solr:8983/solr/admin/cores'
    },
}

BASE_URL = os.getenv('BASE_URL', 'localhost:8000')

try:
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
except KeyError:
    print('Email password not found, email sending not turned on.')
else:
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.mandrillapp.com')
    EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'testing@datamade.us')
    EMAIL_USE_TLS = True

    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
