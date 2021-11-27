import datetime
import os

BASE_DIR = "hseduck_bot"

SQLITE_FILE = "db.sqlite3"
if 'HSEDUCK_DEBUG' in os.environ:
    TICKERS_FILE = os.path.join(BASE_DIR, "data", "tickers_tiny.csv")
else:
    TICKERS_FILE = os.path.join(BASE_DIR, "data", "tickers_medium.csv")
TG_TEMPLATES_FOLDER = os.path.join(BASE_DIR, "telegram_templates")
TG_TOKEN = os.environ['HSEDUCK_TG_TOKEN']
INTERVAL = '1h'
INTERVAL_TIMEDELTA = datetime.timedelta(hours=1)
MAX_FETCH_RANGE = datetime.timedelta(days=31)
PRICE_PRECISION = 1000
PRICE_REPR = "$%.3f"
CURRENCY = 'USD'
INITIAL_BALANCE = 10000
UPDATE_INTERVAL = 60. * 60.
