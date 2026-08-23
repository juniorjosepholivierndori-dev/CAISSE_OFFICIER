from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

postgres_password = os.getenv("POSTGRES_PASSWORD", "").strip()
use_postgres = (
    os.getenv("DB_ENGINE", "sqlite").lower() in {"postgres", "postgresql"}
    and postgres_password
    and postgres_password != "remplace-moi"
)

if use_postgres:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "caisse_gmmg"),
            "USER": os.getenv("POSTGRES_USER", "postgres"),
            "PASSWORD": postgres_password,
            "HOST": os.getenv("POSTGRES_HOST", "127.0.0.1"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
