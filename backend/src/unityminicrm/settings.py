from pathlib import Path

# Local non-settings variables

# Points to the root directory of the repository
_BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Saner defaults

ALLOWED_HOSTS = ["*"]
TIME_ZONE = "UTC"

# (For development only)
SECRET_KEY = " "
DEBUG = True


# "Plugins"

ROOT_URLCONF = "unityminicrm.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "unityminicrm.core",
]

MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware"]


# Peripherals

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": _BASE_DIR / "db.sqlite3",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# `corsheaders` configuration

CORS_ALLOWED_ORIGINS = [
    # (Used by the Vue frontend)
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # (Used by the React frontend)
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]


# `rest_framework` configuration

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated"
    ],
}
