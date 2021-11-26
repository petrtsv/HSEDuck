import datetime
import os

SQLITE_FILE = "db.sqlite3"
TICKERS_FILE = os.path.join("data", "tickers_tiny.csv")
TG_TOKEN = os.environ['HSEDUCK_TG_TOKEN']
INTERVAL = '1h'
MAX_FETCH_RANGE = datetime.timedelta(days=729)
PRICE_PRECISION = 1000
CURRENCY = 'USD'
