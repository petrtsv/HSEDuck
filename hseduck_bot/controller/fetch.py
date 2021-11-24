from hseduck_bot import config
from hseduck_bot.controller import stocks
from hseduck_bot.model.stocks import StockInfo
from hseduck_bot.stocks.api import get_info_by_ticker


def fetch_stocks_info():
    with open(config.TICKERS_FILE, 'r') as tickers_file:
        tickers = [line.strip().upper() for line in tickers_file.readlines() if line and line != "\n"]
    for ticker in tickers:
        info: StockInfo = get_info_by_ticker(ticker)
        if info is not None:
            stocks.save_info(info)

# def fetch_stock_price(ticker: str):
#     stocks.