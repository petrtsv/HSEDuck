from typing import Optional, List

from hseduck_bot import config
from hseduck_bot.controller import transactions
from hseduck_bot.model.portfolios import PortfolioStorage, Portfolio

portfolio_storage: Optional[PortfolioStorage] = None


def initialize(storage: PortfolioStorage):
    global portfolio_storage
    portfolio_storage = storage


def list_portfolios_for_user(user_id: int) -> List[Portfolio]:
    return portfolio_storage.get_portfolios_for_user_id(user_id)


def get_tickers_for_portfolio(portfolio_id: int):
    return portfolio_storage.get_tickers_for_portfolio(portfolio_id)


def create_portfolio(user_id: int, name: str) -> Portfolio:
    new_portfolio = Portfolio(name=name, owner_id=user_id)
    portfolio_storage.create_portfolio(new_portfolio)
    transactions.add_stock(portfolio_id=new_portfolio.id, ticker=config.CURRENCY,
                           quantity=round(config.INITIAL_BALANCE * config.PRICE_PRECISION))
    return new_portfolio


def get_by_id(portfolio_id: int) -> Portfolio:
    return portfolio_storage.get_portfolio_by_id(portfolio_id)
