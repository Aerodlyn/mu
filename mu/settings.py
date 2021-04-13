"""
Django settings for mu project.

Generated by "django-admin startproject" using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import requests

from django.core.management.utils import get_random_secret_key

from distutils.util import strtobool
from pathlib import Path

# https://stackoverflow.com/questions/63011195/how-to-resolve-aws-elastic-beanstalk-django-health-check-problems
def is_ec2_linux():
    if os.path.isfile("/sys/hypervisor/uuid"):
        with open("/sys/hypervisor/uuid") as f:
            uuid = f.read()
            return uuid.startswith("ec2")
    return False

def get_token():
    headers = {
        'X-aws-ec2-metadata-token-ttl-seconds': '21600',
    }
    response = requests.put('http://169.254.169.254/latest/api/token', headers=headers)
    return response.text


def get_linux_ec2_private_ip():
    if not is_ec2_linux():
        return None
    try:
        token = get_token()
        headers = {
            'X-aws-ec2-metadata-token': f"{token}",
        }
        response = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4', headers=headers)
        return response.text
    except:
        return None
    finally:
        if response:
            response.close()

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path (__file__).resolve ().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv ("SECRET_KEY", get_random_secret_key ())

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = strtobool (os.getenv ("DEBUG", "false"))

ALLOWED_HOSTS = os.getenv ("ALLOWED_HOSTS", "").split ()
private_ip = get_linux_ec2_private_ip ()
if private_ip:
    ALLOWED_HOSTS.append (private_ip)

ADMIN_URL = os.getenv ("ADMIN_URL", "admin/")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "crispy_forms",
    "extra_views",
    "rest_framework",

    "forum.apps.ForumConfig",
    "user.apps.UserConfig"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware"
]

ROOT_URLCONF = "mu.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [ "templates" ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages"
            ]
        }
    }
]

WSGI_APPLICATION = "mu.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Whether or not to use RDS as the DB
USE_RDS = os.getenv ("USE_RDS", False)
if USE_RDS:
    DATABASES = {
        "default": {
            "ENGINE": os.getenv ("DB_ENGINE"),
            "HOST": os.getenv ("DB_HOST"),
            "PORT": os.getenv ("DB_PORT"),
            "NAME": os.getenv ("DB_NAME"),
            "USER": os.getenv ("DB_USER"),
            "PASSWORD": os.getenv ("DB_PASS")
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3"
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    }
]

# Login settings
# Login/logout
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/users/login"
LOGOUT_REDIRECT_URL = "/"

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Whether or not to use S3 to store files
USE_S3 = os.getenv ("USE_S3", False)
if USE_S3:
    AWS_ACCESS_KEY_ID = os.getenv ("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv ("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv ("AWS_STORAGE_BUCKET_NAME")
    AWS_IS_GZIPPED = True
    AWS_S3_FILE_OVERWRITE = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATICFILES_DIRS = [
    BASE_DIR / "static"
]

if USE_S3:
    STATICFILES_STORAGE = "mu.backends.StaticStorage"
    STATIC_URL = f"https://{ AWS_STORAGE_BUCKET_NAME }.s3.amazonaws.com/static/"
else:
    STATIC_URL = "/static/"

# Media files
# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-MEDIA_ROOT
if USE_S3:
    DEFAULT_FILE_STORAGE = "mu.backends.MediaStorage"
    MEDIA_URL = f"https://{ AWS_STORAGE_BUCKET_NAME }.s3.amazonaws.com/media/"
else:
    MEDIA_ROOT = BASE_DIR / "media"
    MEDIA_URL = "/media/"

# Crispy Forms
CRISPY_TEMPLATE_PACK = "bootstrap4"
