import os
import environ
from pathlib import Path

env = environ.Env(DEBUG=(bool, False), ALLOWED_HOSTS=(str, "*"), TIME_ZONE=(str, "Africa/Nairobi"))
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",") if isinstance(env("ALLOWED_HOSTS"), str) else ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "django_filters",
    "mptt",
    "accounts",
    "catalog",
    "orders",
    "notifications",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware","django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"
TEMPLATES = [{
  "BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[],"APP_DIRS":True,
  "OPTIONS":{"context_processors":[
    "django.template.context_processors.debug","django.template.context_processors.request",
    "django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}
}]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {"default":{
    "ENGINE":"django.db.backends.postgresql",
    "NAME": env("POSTGRES_DB"),
    "USER": env("POSTGRES_USER"),
    "PASSWORD": env("POSTGRES_PASSWORD"),
    "HOST": env("POSTGRES_HOST"),
    "PORT": env("POSTGRES_PORT"),
}}

LANGUAGE_CODE = "en-us"
TIME_ZONE = env("TIME_ZONE", default="Africa/Nairobi")
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {

  "DEFAULT_AUTHENTICATION_CLASSES":["rest_framework_simplejwt.authentication.JWTAuthentication"],
  "DEFAULT_PERMISSION_CLASSES":["rest_framework.permissions.IsAuthenticated"],
  "DEFAULT_FILTER_BACKENDS":[
    "django_filters.rest_framework.DjangoFilterBackend",
    "rest_framework.filters.OrderingFilter",
    "rest_framework.filters.SearchFilter"
  ],
}



# Email (MailHog)
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="mailhog"
EMAIL_PORT=1025
EMAIL_USE_TLS=False
DEFAULT_FROM_EMAIL="noreply@sil.com"
ADMIN_EMAIL=env("ADMIN_EMAIL", default="admin@example.com")

# Africa's Talking
AT_USERNAME=env("AT_USERNAME", default="sandbox")
AT_API_KEY=env("AT_API_KEY", default="")
AT_SENDER_ID=env("AT_SENDER_ID", default="SENDER")

# Google OIDC settings (set via env vars)
OIDC_ISSUER = os.getenv("OIDC_ISSUER")
OIDC_CLIENT_ID = os.getenv("OIDC_CLIENT_ID")
OIDC_CLIENT_SECRET = os.getenv("OIDC_CLIENT_SECRET")
OIDC_REDIRECT_URI = os.getenv("OIDC_REDIRECT_URI")

# Comma-separated list of admin emails (quick admin mapping method)
OIDC_ADMIN_EMAILS = os.getenv("OIDC_ADMIN_EMAILS", "")  # e.g. "boss@example.com,admin@org.com"

# Discovery doc & cache TTL (seconds)
OIDC_DISCOVERY_URL =  f"{OIDC_ISSUER}/.well-known/openid-configuration"
OIDC_CACHE_TTL = int(os.getenv("OIDC_CACHE_TTL", "300"))


