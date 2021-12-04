import json
from typing import Optional

import yfinance as yf

from hseduck_bot.model.stocks import StockInfo


def get_info_by_ticker(ticker_str: str) -> Optional[StockInfo]:
    ticker = yf.Ticker(ticker_str)
    if ticker is None:
        return None
    info = ticker.info
    try:
        return StockInfo(ticker=ticker_str, name=info['shortName'], description=info['longBusinessSummary'],
                         json_info=json.dumps(info))
    except KeyError:
        return None
