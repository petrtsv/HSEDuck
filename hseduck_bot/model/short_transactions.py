import datetime
from abc import ABC, abstractmethod
from typing import Optional, List, Iterable

from hseduck_bot.model.transactions import Transaction


class ShortTransaction(Transaction):
    def __init__(self, portfolio_id: int, quantity: int, ticker: str, timestamp: datetime.datetime,
                 transaction_id: int = None):
        super().__init__(portfolio_id, quantity, ticker)
        self.timestamp = timestamp
        self.id = transaction_id


class ShortTransactionStorage(ABC):
    @abstractmethod
    def add_short_transaction_batch(self, batch: Iterable[ShortTransaction]) -> None:
        pass

    @abstractmethod
    def get_ready_short_transactions(self, timestamp: Optional[datetime.datetime] = None) -> List[ShortTransaction]:
        pass

    @abstractmethod
    def remove_short_transaction(self, transaction_id: int) -> None:
        pass

    @abstractmethod
    def get_current_shorts(self, portfolio_id: int) -> List[ShortTransaction]:
        pass
