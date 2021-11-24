from abc import ABC, abstractmethod
from typing import Optional, Iterable


class Transaction:
    def __init__(self, portfolio_id: int, quantity: int, ticker: str):
        self.portfolio_id = portfolio_id
        self.quantity = quantity
        self.ticker = ticker


class TransactionStorage(ABC):
    @abstractmethod
    def add_transaction_batch(self, batch: Iterable[Transaction]):
        pass

    @abstractmethod
    def get_quantity(self, portfolio_id: int, ticker: str) -> int:
        pass
