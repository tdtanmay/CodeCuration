from .settings_local import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'blog_db_prod',
        'USER': 'tanmay',
        'PASSWORD': '123',
        'PORT': '5432',
    }
}