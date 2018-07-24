
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myblog_db',
        'USER': 'tanmay',
        'PASSWORD': 'tanmay@52236',
        'PORT': '5432',
    }
}
