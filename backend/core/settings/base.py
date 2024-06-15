import environ

from pathlib import Path
from datetime import timedelta

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
ROOT_DIR = Path(__file__).resolve().parent.parent.parent  # 3 parents pointing to the root dir

APP_DIR = ROOT_DIR / "apps"
# Application definition

DEBUG = env.bool("DJANGO_DEBUG", False)

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites"
]
THIRD_PARTY_APPS = [
    "rest_framework", 
    "corsheaders", 
    "django_countries",  
    "phonenumber_field", 
    "drf_yasg",
    "djcelery_email",
    "rest_framework.authtoken",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    # "django_elasticsearch_dsl",
    # "django_elasticsearch_dsl_drf",
    # "storages",
    ]

LOCAL_APPS = [
    "apps.common",
    "apps.branches",
    "apps.currencies",
    "apps.users",  
    "apps.profiles",
    "apps.audits",
    "apps.branch_assets",   
    "apps.periods",  
    "apps.products",
    "apps.branch_products",
    "apps.groups",
    "apps.group_product",
    "apps.clients",
    "apps.employers",
    "apps.loan_statuses",
    "apps.charges",
    "apps.group_product_charge",
    "apps.branch_product_charge",
    "apps.payment_gateways",
    "apps.finance",
    "apps.loan_applications",
    "apps.global_settings",
    "apps.branch_settings",
    "apps.documents",
    "apps.document_types",
    # "apps.smses",
    # "apps.emails",
    # "apps.notifications",
    "apps.loans",
    "apps.loan_transactions",
    # "apps.search"
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    # "whitenoise.middleware.WhiteNoiseMiddleware",# PRODUCTION ONLY
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Harare"

USE_I18N = True

USE_TZ = True

SITE_ID = 1 

ADMIN_URL = "supersecret/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/staticfiles/'
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
STATICFILES_DIR = []
MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = str(ROOT_DIR/ "mediafiles")

# AWS_QUERYSTRING_AUTH = False
# AWS_ACCESS_KEY_ID=env("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY=env("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME=env("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_FILE_OVERWRITE = False
# AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage" # This is for Django <4.2
# STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.s3.S3Storage", # This is for Django >=4.2 
#     },
#     "staticfiles": {
#         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
#     }
# }




# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_URLS_REGEX = r"^/api/.*$" # CORS added to all API endpoints

DATABASES = {"default": env.db("DATABASE_URL")}

AUTH_USER_MODEL = "users.User" #We are telling django the location of our custom user 

CELERY_BROKER_URL = env("CELERY_BROKER")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
CELERY_TASK_SEND_SENT_EVENT = True

if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE

ALLOWED_HOSTS = ["*"]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",  #This will set cookies and set refresh_token to empty on login
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],  
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "SIGNING_KEY": env("SIGNING_KEY"),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

REST_AUTH = {
    "USE_JWT":True,
    "JWT_AUTH_COOKIE": "microfinex-acces-token",
    "JWT_AUTH_REFRESH_COOKIE": "microfinex-refresh-token",
    "REGISTER_SERIALIZER": "apps.users.serializers.CustomRegisterSerializer"
}


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = False
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1

ELASTICSEARCH_DSL ={
    "default":{
        'hosts':"es:9200", # From dockerfile container
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(name)-12s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }      
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },        
    },
   "root": {
       "level": "INFO",
       "handlers": ["console"],
   }
}

CORS_ALLOWED_ORIGINS = ["http://localhost:3000","http://127.0.0.1:3000"]
CORS_ALLOW_CREDENTIALS = True
ACCOUNT_ADAPTER = "apps.users.auth_emails.CustomAccountAdapter"


