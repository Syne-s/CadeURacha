import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-m7nz^1020$)xzc1y6r9r5z890@%ni7^&6+^@0@k2c*n@3zq!qi')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['cade-u-racha.up.railway.app', 'localhost', '127.0.0.1', 'cadeuracha.up.railway.app']

CSRF_TRUSTED_ORIGINS = ['https://cade-u-racha.up.railway.app']

CORS_ALLOWED_ORIGINS = ['https://cade-u-racha.up.railway.app']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_synes',
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Adicione esta linha
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app_synes.middleware.UsernameValidationMiddleware',
]

ROOT_URLCONF = 'synes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

WSGI_APPLICATION = 'synes.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'eLBxoXfIyqiYwRxBRSxjNLZtOTsgowRu',
        'HOST': 'autorack.proxy.rlwy.net',
        'PORT': '37107',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Fortaleza'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'app_synes/static'),
]

# Diretório onde os arquivos estáticos serão coletados
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configurações do WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# URL para acessar arquivos de mídia
MEDIA_URL = '/media/'

# Diretório local para armazenar arquivos temporariamente (não utilizado no CloudinaryStorage)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Cloudinary settings
CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

# Configurar o Cloudinary como storage padrão para arquivos de mídia
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Configuração para limpar arquivos temporários
CLOUDINARY_DELETE_AFTER_UPLOAD = True

# Pasta temporária para uploads, que será limpa periodicamente
TEMP_UPLOAD_ROOT = os.path.join(BASE_DIR, 'temp_uploads')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'app_synes.CustomUser'

# Certifique-se de que DEBUG está definido como True em desenvolvimento
DEBUG = True
