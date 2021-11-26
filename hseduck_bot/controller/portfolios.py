from typing import Optional, List

from hseduck_bot.model.portfolios import PortfolioStorage, Portfolio

portfolio_storage: Optional[PortfolioStorage] = None


def initialize(storage: PortfolioStorage):
    global portfolio_storage
    portfolio_storage = storage


def list_portfolios_for_user(user_id: int) -> List[Portfolio]:
    return portfolio_storage.get_portfolios_for_user_id(user_id)


def get_tickers_for_portfolio(portfolio_id: int):
    return portfolio_storage.get_tickers_for_portfolio(portfolio_id)
