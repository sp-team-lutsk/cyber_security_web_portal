import datetime
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#-+2%cfp05=)8q*u1s2itkffi$i^@ir5@bv%!9g3irbfi_)2h5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Update in prod it
ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 
    'django.contrib.sites',
    
    'rest_framework',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django_nose',

    'djangotoolbox',
    'authentication',
]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
AUTH_USER_MODEL = 'authentication.StdUser'


AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
)
# social_django provider settings
USE_UNIQUE_USER_ID = True
SOCIAL_AUTH_FACEBOOK_KEY = '2293012740916243'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'b9fa3a771d57fba2b045886162e5b685'  # App Secret
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '139031750986-d7jnj1ogdmtbg271bsegbiafj6qrshlb.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'A8KihEKp4CiiM7rJnRqFYWYb'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'social_django.context_processors.backends',  
                'social_django.context_processors.login_redirect', 
            ],

        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgresql',
        'USER': 'admin',
        'PASSWORD': 'Admin123!',
        'HOST': 'postgresql',
        'PORT': '5432',# if you use docker you should specify  'HOST': 'mongodb', but if it is locally 'HOST': '127.0.0.1'
    }
}

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS':{
            'min_length':8,
            }
    
    },
    
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    
    {
        'NAME': 'authentication.validators.SymbolPasswordValidator',
    
    },
    
    {
        'NAME': 'authentication.validators.CharPasswordValidator',

    },
    
    {
        'NAME': 'authentication.validators.UpPasswordValidator',

    },
    {
        'NAME': 'authentication.validators.LowPasswordValidator',

    },
]

# settings for rest framework
REST_FRAMEWORK = {
  
#JWT 
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
#Permissions
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAdminUser'
        
    ),
}

# JWT auth parameters
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=14)
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
# Media files

MEDIA_ROOT = os.path.join(BASE_DIR, 'media_files')
MEDIA_URL = '/media/'
REST_USE_JWT = True

# providers settings
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.12',
    },
     'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# allauth user relation
SOCIALACCOUNT_QUERY_EMAIL = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# redirect urls
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL ='/accounts/login/'

SITE_ID = 2
