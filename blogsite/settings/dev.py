from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i=lb&_gh7asj3tx=vpn!7cd$v)!ad#2q*e9pc@at^*ywyhh&_+'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CSRF_TRUSTED_ORIGINS = ['https://*.127.0.0.1', 'https://www.wangfamily.eu.org']

try:
    from .local import *
except ImportError:
    pass
