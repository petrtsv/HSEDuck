import datetime
from typing import Optional, List

from hseduck_bot import config
from hseduck_bot.controller import transactions, stocks
from hseduck_bot.model.short_transactions import ShortTransactionStorage, ShortTransaction

short_transaction_storage: Optional[ShortTransactionStorage] = None


def initialize(storage: ShortTransactionStorage):
    global short_transaction_storage
    short_transaction_storage = storage


def execute_short_transaction(transaction: ShortTransaction):
    current_quantity = transactions.quantity_in_portfolio(transaction.portfolio_id, transaction.ticker)
    delta = transaction.quantity - current_quantity

    if delta > 0:
        transactions.buy_stock(portfolio_id=transaction.portfolio_id,
                               ticker=transaction.ticker,
                               quantity=delta,
                               ignore_amount=True)

    transactions.add_stock(portfolio_id=transaction.portfolio_id,
                           ticker=transaction.ticker,
                           quantity=-transaction.quantity)
    short_transaction_storage.remove_short_transaction(transaction_id=transaction.id)


def update() -> None:
    short_transactions = short_transaction_storage.get_ready_short_transactions()
    for short_transaction in short_transactions:
        execute_short_transaction(short_transaction)


def get_current_shorts(portfolio_id: int) -> List[ShortTransaction]:
    return short_transaction_storage.get_current_shorts(portfolio_id)


class ShortsLimitExceeded(Exception):
    def __init__(self, limit: int, try_to_get: int):
        super(ShortsLimitExceeded, self).__init__()
        self.limit = limit
        self.try_to_get = try_to_get


def short_stock(portfolio_id: int, ticker: str, quantity: int,
                duration: datetime.timedelta = config.SHORT_DURATION) -> None:
    shorts_cost_after = shorts_cost_in_portfolio(portfolio_id, as_int=True) + stocks.price_int(ticker) * quantity
    if shorts_cost_after > config.SHORT_MAX_NOT_COVERED * config.PRICE_PRECISION:
        raise ShortsLimitExceeded(limit=config.SHORT_MAX_NOT_COVERED,
                                  try_to_get=shorts_cost_after / config.PRICE_PRECISION)

    end_date = datetime.datetime.now() + duration
    transactions.add_stock(portfolio_id, ticker, quantity)
    transactions.sell_stock(portfolio_id, ticker, quantity)
    transaction = ShortTransaction(portfolio_id=portfolio_id, quantity=quantity, ticker=ticker, timestamp=end_date)
    short_transaction_storage.add_short_transaction_batch([transaction])


def shorts_cost_in_portfolio(portfolio_id, as_int=False):
    total_cost = 0
    for short in get_current_shorts(portfolio_id):
        if as_int:
            total_cost += short.quantity * stocks.price_int(short.ticker)
        else:
            total_cost += short.quantity * stocks.price_float(short.ticker)
    return total_cost
