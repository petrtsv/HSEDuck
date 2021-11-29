from abc import ABC, abstractmethod
from typing import Optional, List

from hseduck_bot.model.users import User


class Portfolio:
    def __init__(self, name: str, owner_id: int, portfolio_id: int = None):
        self.id = int(portfolio_id) if portfolio_id is not None else None
        self.owner_id = int(owner_id)
        self.name = name


class PortfolioStorage(ABC):
    @abstractmethod
    def create_portfolio(self, portfolio: Portfolio) -> None:
        pass

    @abstractmethod
    def get_portfolio_by_id(self, portfolio_id: int) -> Optional[Portfolio]:
        pass

    @abstractmethod
    def get_portfolios_for_user_id(self, user_id: int) -> List[Portfolio]:
        pass

    @abstractmethod
    def get_tickers_for_portfolio(self, portfolio_id) -> List[str]:
        pass
