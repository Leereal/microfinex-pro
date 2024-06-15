from .base import * #noqa
from .base import env
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY", default="bWjYw3sb03X-ZllnYhvntFZ3RF_5LxORWBzKaAvcfw6haA6EUBg")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080","http://172.25.241.154:8080"]

DB_USERNAME = env("POSTGRES_USER")
DB_PASSWORD = env("POSTGRES_PASSWORD")
DB_DATABASE = env("POSTGRES_DB")
DB_HOST = env("POSTGRES_HOST")
DB_PORT = env("POSTGRES_PORT")

# DB_USERNAME = POSTGRES_USER="leereal"
# DB_PASSWORD = POSTGRES_PASSWORD="mutabvuri$8"
# DB_DATABASE = POSTGRES_DB="microfinex-dev"
# DB_HOST = POSTGRES_HOST="localhost"
# DB_PORT = POSTGRES_PORT=5432

DB_IS_AVAIL = all([
    DB_USERNAME,
    DB_PASSWORD,
    DB_DATABASE,
    DB_HOST,
    DB_PORT
])

if DB_IS_AVAIL:
    DATABASES = {
        'default': {
            "ENGINE": 'django.db.backends.postgresql',
            "NAME": DB_DATABASE,
            "USER": DB_USERNAME,
            "PASSWORD": DB_PASSWORD,
            "HOST":DB_HOST,
            "PORT": DB_PORT,
            'OPTIONS': {
      'sslmode': 'require',
    },
        }
    }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'microfinex',
#         'USER': 'leereal',
#         'PASSWORD': 'mutabvuri$8',
#         'HOST': 'microfinex.ch0o6skwcb06.us-east-1.rds.amazonaws.com',
#         'PORT': '5432',
#     }
# }

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = env("EMAIL_PORT")
DEFAULT_FROM_EMAIL = "leereal08@ymail.com"
DOMAIN = env("DOMAIN")
SITE_NAME = "Microfinex Pro"