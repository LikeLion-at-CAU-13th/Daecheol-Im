"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
# 파일을 읽기 위해 필요한 라이브러리를 설치합니다.
from pathlib import Path
import os, json
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

secret_file = os.path.join(BASE_DIR, 'secrets.json') 

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets): 
# secret 변수를 가져오거나 그렇지 못 하면 예외를 반환
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'posts',
    'accounts',
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
]


INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # 반드시 가장 위쪽에 추가
    'posts.logging_middleware.RequestLoggingMiddleware',
    #기본 미들웨어
    'django.middleware.security.SecurityMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'

# 인증 관련 요청(쿠키, 세션 등)을 허용
# 예를 들어 브라우저가 백엔드 서버로 쿠키를 전송하거나, 백엔드에서 쿠키를 응답으로 보낼 수 있음
CORS_ALLOW_CREDENTIALS = True

# 서버로 요청 보낼 수 있는 도메인들 정의
# 여기에서의 localhost는 EC2 인스턴스의 로컬환경이 아니라 프론트엔드 개발 로컬 환경 의미
# 3000 포트는 프론트엔드 React 애플리케이션의 포트 번호
# 추후 프론트엔드에서 웹 페이지 배포 후 도메인 매핑했다면 해당 도메인 추가 필요
CORS_ALLOWED_ORIGINS = [ 
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# 로그 기록

LOG_DIR = os.path.join(BASE_DIR, 'logs') # 로그 파일을 저장할 디렉토리를 BASE_DIR/logs로 설정
os.makedirs(LOG_DIR, exist_ok=True) # logs 폴더가 없으면 자동 생성

LOGGING = {
    'version' : 1,
    'disable_existing_loggers': False,
    'formatters' : {
        'standard' : {
            'format' : '[{asctime}] {levelname} {message}',
            'style' : '{',
        },
        'detailed': {
            'format': '[{asctime}] {levelname} {name} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file_all': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'all_requests.log'),
            'formatter': 'standard',
        },
        'file_errors': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'errors.log'),
            'formatter': 'detailed',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file_all', 'file_errors'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['file_all', 'file_errors'],
            'level': 'INFO',
            'propagate': False,
        },   
    },
}
