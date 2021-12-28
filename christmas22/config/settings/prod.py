from .base import *

import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('PROD_DATABASE_NAME'),
        'USER': get_secret('PROD_DATABASE_USER'),
        'PASSWORD': get_secret('PROD_DATABASE_PASSWORD'),
        'HOST': get_secret('PROD_DATABASE_HOST'),
        'PORT': get_secret('PROD_DATABASE_PORT')
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'Christmas2021/static')
STATIC_URL = 'https://christmas.jatmorris.org/static/'
STATICFILES_DIRS = ( os.path.join(BASE_DIR, 'static', 'site',), )

ALLOWED_HOSTS = ['christmas.jatmorris.org',
                 'www.christmas.jatmorris.org']

# ADMINS = (
    # ('Jim', 'jmorris@ecybermind.net'), ('Jim', 'frjamesmorris@gmail.com')
# )

EMAIL_HOST = get_secret('EMAIL_HOST')
EMAIL_PORT = get_secret('EMAIL_PORT')
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = get_secret('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = get_secret('SERVER_EMAIL')
EMAIL_USE_TLS = True
