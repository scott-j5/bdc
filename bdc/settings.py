"""
Django settings for bdc project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get('DJANGO_DEBUG'))

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Application definition
SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'accounts',
    'allauth',
	# replaced: "allauth.account" to prevent migration issue on default_auto_field
    "bdc.apps.ModifiedAccountConfig",
    # replaced: "allauth.socialaccount" to prevent migration issue on default_auto_field
    "bdc.apps.ModifiedSocialAccountConfig",
	"blogs",
	'allauth.socialaccount.providers.google',
	'bootstrap_modal',
	'captcha',
	'crispy_forms',
	'crispy_bootstrap5',
    'core',
	'dashboard',
	'faq',
	'imageit',
	'invoicing',
	'mapbox_location_field',
	'products',
	'rentals',
	'vans',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bdc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': ['core/templates'],   
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
				'core.context_processors.vans',
				'rentals.context_processors.charge_period',
            ],
        },
    },
]

WSGI_APPLICATION = 'bdc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql',
			'NAME': os.environ.get('DATABASE_NAME'),
			'USER': os.environ.get('DATABASE_USER'),
			'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
			'HOST': os.environ.get('DATABASE_HOST'),
			'PORT': '5432'
		}
	}

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    }
DATABASE_SIZE = "40GB"

#Auth backends
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = ('bootstrap', 'uni_form', 'bootstrap3', 'bootstrap4', 'bootstrap5', )
CRISPY_TEMPLATE_PACK = 'bootstrap5'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# Where to look for static files during collect static
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'dist'),
]

#Where 'collectstatic' dumps static files
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'staticfiles')

#URL prefix used by static template tags
STATIC_URL = '/dist/'

if not DEBUG:
# S3 folder to upload static files to
    STATICFILES_LOCATION = 'static'
    STATICFILES_STORAGE = 'static_storages.StaticStorage'



#Email settings
DEFAULT_FROM_EMAIL = 'noreply@bigdogcampers.co.uk'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com.au'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
SERVER_EMAIL = os.environ.get('EMAIL_USER')
SEND_BROKEN_LINK_EMAILS = True

ADMINS = [
	("Scott", "admin@byitegroup.com"),
	("Scott", "scotty.james95@gmail.com")
]
MANAGERS = [
	("Scott", "admin@byitegroup.com"),
	("Scott", "scotty.james95@gmail.com")
]


# RECAPTCHA SETTINGS
RECAPTCHA_PUBLIC_KEY = '6Ley4cEeAAAAAAAoUsibytP95zsTJE2RY7pofyEs'
RECAPTCHA_PRIVATE_KEY = '6Ley4cEeAAAAAFnw96Y_UaU_BOKqT0F1o_G6nkpv'


#S3 storage settings
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

# S3 folder to upload media files to
MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'media_storages.MediaStorage'


# TO BE DELETED ONCE ALLAUTH DEFAULT_AUTO_FIELD UPDATES ARE RELEASED
import allauth.app_settings
allauth.app_settings.SOCIALACCOUNT_ENABLED = True


SOCIALACCOUNT_PROVIDERS = {
	'google': {
		# For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

ACCOUNT_PRESERVE_USERNAME_CASING = False

ACCOUNT_USER_DISPLAY = 'accounts.utils.user_display_name'


DJRICHTEXTFIELD_CONFIG = {
    'js': ['https://cdn.tiny.cloud/1/zsce7lst5im33auwvlcxynn7rqyiwyopckmqdtjxebwsp8x2/tinymce/5/tinymce.min.js'],
    'init_template': 'core/init-tinymce.js',
    'settings': {
        'menubar': False,
        'plugins': 'code codesample hr image lists link table',
        'toolbar': [
            'code | undo redo | styleselect | bold italic underline hr | alignleft aligncenter alignright alignjustify | outdent indent | numlist bullist',
            'codesample image link | table tabledelete | tableprops tablerowprops tablecellprops | tableinsertrowbefore tableinsertrowafter tabledeleterow | tableinsertcolbefore tableinsertcolafter tabledeletecol',
        ],
        'codesample_languages': [
            {'text': 'Bash', 'value': 'bash' },
            {'text': 'Apache', 'value': 'apacheconf' },
            {'text': 'C', 'value': 'c' },
            {'text': 'C#', 'value': 'csharp' },
            {'text': 'C++', 'value': 'cpp' },
            {'text': 'CSS', 'value': 'css' },
            {'text': 'F#', 'value': 'fsharp' },
            {'text': 'Java', 'value': 'java'},
            {'text': 'HTML/XML', 'value': 'markup'},
            {'text': 'JavaScript', 'value': 'javascript' },
            {'text': 'Json', 'value': 'json' },
            {'text': 'LESS', 'value': 'less' },
            {'text': 'PHP', 'value': 'php'},
            {'text': 'Python', 'value': 'python'},
            {'text': 'Ruby', 'value': 'ruby'},
            {'text': 'SASS', 'value': 'scss' },
            {'text': 'SQL', 'value': 'sql' },
            {'text': 'TypeScript', 'value': 'typescript' }
        ],
        'width': '100%',
        'height': '500',
        'branding': False,
        'images_upload_url': '/blogs/blog/default/image/upload/',
        'relative_urls': False,
    }
}

MAPBOX_KEY = 'pk.eyJ1Ijoic2NvdHQtajUiLCJhIjoiY2wyYjlpenR2MDBrbjNpb3BxY3BuNjdsaSJ9.loR_ycWP28bIMtm5qiL1pw'