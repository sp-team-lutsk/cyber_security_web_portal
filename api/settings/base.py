import datetime
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'static'))

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
    'rest_framework.authtoken', 
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

    'djangotoolbox',
<<<<<<< HEAD:api/settings/base.py
    'authentication',
=======
    'pages',
    
>>>>>>> master:settings/base.py
]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
AUTH_USER_MODEL = 'authentication.StdUser'

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

LOGIN_REDIRECT_URL = 'home'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, '/static/templates'),
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
            ],

        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'mongodb',
        'HOST': 'mongodb',   # if you use docker you should specify  'HOST': 'mongodb', but if it is locally 'HOST': '127.0.0.1'
    }
}

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
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

MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')
MEDIA_URL = '/media/'


# Static files (CSS, JavaScript, Images)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SITE_ID = 2
