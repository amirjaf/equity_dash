# package imports
import os
from dotenv import load_dotenv

cwd = os.getcwd()
dotenv_path = os.path.join(cwd, os.getenv("ENVIRONMENT_FILE", ".env.development"))
load_dotenv(dotenv_path=dotenv_path, override=True)

APP_HOST = os.environ.get("HOST")
APP_PORT = int(os.environ.get("PORT"))
APP_DEBUG = bool(os.environ.get("DEBUG"))
USE_RELOADER = bool(os.environ.get("USE_RELOADER"))
DEV_TOOLS_PROPS_CHECK = bool(os.environ.get("DEV_TOOLS_PROPS_CHECK"))
API_KEY = os.environ.get("API_KEY", None)
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_PORT = int(os.environ.get("POSTGRES_PORT"))
DB_HOST = os.environ.get("DB_HOST")
POSTGRES_SCHEMA = os.environ.get("POSTGRES_SCHEMA")
TOUR_TABLE_NAME = os.environ.get("TOUR_TABLE_NAME")
TRIP_TABLE_NAME = os.environ.get("TRIP_TABLE_NAME")
