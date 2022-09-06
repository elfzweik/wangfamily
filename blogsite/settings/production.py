from .base import *

DEBUG = False

CSRF_TRUSTED_ORIGINS = ['https://blog.petal2collect.ml','https://*.127.0.0.1','https://www.petal2collect.ga', 'https://www.wangfamily.ga']

try:
    from .local import *
except ImportError:
    pass
