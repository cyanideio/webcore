# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_ENV = os.environ['MANIFEST_ENV']
PASSWORD = os.environ['DJANGO_PASS']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')5&81@cr19@4e2*0oeg%peiru@s(+x3rzmau(k!bz*tf*l@j67'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['2501.vaul.tech']

# Application definition

INSTALLED_APPS = (
    # Custom Applications
    'core.apps.CoreConfig',              # The Core Application
    'grappelli.dashboard',
    # Third Party Applications
    'grappelli',
    'filebrowser',
    'taggit',                            # Django-Taggit
    'tastypie',                          # Django-Tastypie
    'autofixture',                       # Testing Model
    # Django Defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'admin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'manifest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# if program runs on local
if MANIFEST_ENV == 'local':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# if program runs on server
elif MANIFEST_ENV == 'server':
    DATABASES = {
            'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'webcore',                      
            'USER': 'webcore',
            'PASSWORD': PASSWORD,
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# TASTYPIE Default Format
TASTYPIE_DEFAULT_FORMATS = ['json']

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = False

USE_L10N = True

USE_TZ = True

GRAPPELLI_ADMIN_TITLE = 'Cyanide.io'

MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

if MANIFEST_ENV == 'server':
    STATIC_ROOT = '/usr/share/nginx/static'
    MEDIA_ROOT = '/usr/share/nginx/media'
