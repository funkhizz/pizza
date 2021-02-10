"""
Django settings for pizza_online project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = Path(__file__).resolve().parents[0]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "&dhi-62rv&-0++!gxttvlrb!3mxnr&nq5xe8%$$b1m6_t*rg8m"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
ROOT_URLCONF = "pizza_online.urls"


CLIENT_NAME = "Pizza Online"
SUPPORT_EMAIL = "digital.accounts@pizza-online.com"

DEFAULT_FROM_EMAIL = "{0} <corporate.communcations@pizza-online.com>".format(
    CLIENT_NAME
)

WEB_DEV_STAFF = [
    "vl.hizz@gmail.com"
]

CLIENT_STAFF = [
    "sam.mitchel@pizza-online.com",
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pipeline",
    "custom_user",
    'crispy_forms',
    "pizza_online.apps.products.apps.ProductsConfig",
    "pizza_online.apps.ingredients.apps.IngredientsConfig",
    "pizza_online.apps.carts.apps.CartsConfig",
    "pizza_online.apps.users.apps.UsersConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pizza_online.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_DIR / "templates"],
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

WSGI_APPLICATION = "pizza_online.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

# AUTH
AUTH_USER_MODEL = "users.User"

# Login
LOGIN_URL = "users:login-or-register"
LOGIN_REDIRECT_URL = "users:home"


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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_STORAGE = "pipeline.storage.PipelineStorage"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "pipeline.finders.PipelineFinder",
)

STATIC_ROOT = PROJECT_DIR / "staticfiles"
STATIC_URL = "/static/"

STATICFILES_DIRS = (PROJECT_DIR / "static",)

MEDIA_ROOT = PROJECT_DIR / "uploads"
MEDIA_URL = "/uploads/"
# django-pipeline
# ----------------------------
PIPELINE = {
    "STYLESHEETS": {
        "base": {
            "source_filenames": ("scss/base.scss",),
            "output_filename": "css/base.min.css",
        },
        "home": {
            "source_filenames": ("scss/pages/home.scss",),
            "output_filename": "css/pages/home.min.css",
        },
        "menu-list": {
            "source_filenames": ("scss/pages/menu-list.scss",),
            "output_filename": "css/pages/menu-list.min.css",
        },
        "pizza-detail": {
            "source_filenames": ("scss/pages/pizza-detail.scss",),
            "output_filename": "css/pages/pizza-detail.min.css",
        },
        "cart-home": {
            "source_filenames": ("scss/pages/cart-home.scss",),
            "output_filename": "css/pages/cart-home.min.css",
        },
        "login-or-register": {
            "source_filenames": ("scss/pages/login-or-register.scss",),
            "output_filename": "css/pages/login-or-register.min.css",
        },
    },
    "JAVASCRIPT": {
        "global": {
            "source_filenames": ("js/libs/jQuery-3.5.1.js", "js/global.js"),
            "output_filename": "js/jQuery-3.5.1.min.js",
        },
        "pizza-detail": {
            "source_filenames": ("js/pages/pizza-detail.js",),
            "output_filename": "js/pizza-detail.min.js",
        },
        "update-item": {
            "source_filenames": ("js/pages/update-item.js",),
            "output_filename": "js/update-item.min.js",
        },
    },
    "COMPILERS": ("pipeline.compilers.sass.SASSCompiler",),
    "SASS_BINARY": "pysassc",
    "SASS_ARGUMENTS": "--sourcemap",
    "JS_COMPRESSOR": "pipeline.compressors.NoopCompressor",
    "DISABLE_WRAPPER": True,
}
