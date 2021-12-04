import datetime
import math
from typing import Optional

import yfinance as yf

from hseduck_bot import config
from hseduck_bot.controller import stocks
from hseduck_bot.model.stocks import StockInfo, StockRecord
from hseduck_bot.stocks.api import get_info_by_ticker


def fetch_stocks_info():
    with open(config.TICKERS_FILE, 'r') as tickers_file:
        tickers = [line.strip().upper() for line in tickers_file.readlines() if line and line != "\n"]
    for ticker in tickers:
        info: StockInfo = get_info_by_ticker(ticker)
        if info is not None:
            stocks.save_info(info)


def fetch_stock_prices(ticker: str, start: Optional[datetime.datetime] = None):
    min_start = datetime.datetime.now() - config.MAX_FETCH_RANGE
    if start is None or start < min_start:
        start = min_start
    start += config.INTERVAL_TIMEDELTA
    data = yf.download(ticker, start=start, end=datetime.datetime.now(),
                       group_by="ticker", progress=False, interval=config.INTERVAL, show_errors=False)
    for row in data.iterrows():
        if not math.isnan(row[1]['Close']):
            stocks.save_record(StockRecord(ticker, round(row[1]['Close'] * config.PRICE_PRECISION), row[0]))
