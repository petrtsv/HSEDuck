import datetime
import os

DEBUG = 'HSEDUCK_DEBUG' in os.environ

BASE_DIR = "hseduck_bot"

if DEBUG:
    DB_TYPE = "sqlite"
    CONNECTION_STRING = "db.sqlite3"
else:
    DB_TYPE = "postgres"
    CONNECTION_STRING = os.environ['DATABASE_URL']

if DEBUG:
    TICKERS_FILE = os.path.join(BASE_DIR, "data", "tickers_tiny.csv")
else:
    TICKERS_FILE = os.path.join(BASE_DIR, "data", "tickers_medium.csv")

TG_TEMPLATES_FOLDER = os.path.join(BASE_DIR, "telegram_templates")
TG_TOKEN = os.environ['HSEDUCK_TG_TOKEN']
INTERVAL = '1h'
INTERVAL_TIMEDELTA = datetime.timedelta(hours=1)
MAX_FETCH_RANGE = datetime.timedelta(days=7)
PRICE_PRECISION = 1000
PRICE_REPR = "$%.3f"
CURRENCY = 'USD'
INITIAL_BALANCE = 10000
UPDATE_STOCKS_INTERVAL = 60 * 60 * 1
UPDATE_DB_INTERVAL = 30 * 1

GLOBAL_CONTEST_OWNER_USERNAME = "@@@GLOBAL_CONTEST_OWNER@@@"
GLOBAL_COMPETITION_DURATION = datetime.timedelta(days=366 * 1000)
GLOBAL_COMPETITION_NAME = "GLOBAL"
GLOBAL_CONTEST_ALIAS = "global"

if DEBUG:
    SHORT_DURATION = datetime.timedelta(minutes=5)
else:
    SHORT_DURATION = datetime.timedelta(hours=24)
SHORT_MAX_NOT_COVERED = 10000
