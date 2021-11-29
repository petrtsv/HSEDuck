from typing import Optional

from hseduck_bot import config
from hseduck_bot.controller.stocks import price_int
from hseduck_bot.model.transactions import TransactionStorage, Transaction

transaction_storage: Optional[TransactionStorage] = None


def initialize(storage: TransactionStorage):
    global transaction_storage
    transaction_storage = storage


def quantity_in_portfolio(portfolio_id: int, ticker: str):
    return int(transaction_storage.get_quantity(portfolio_id, ticker))


class NotEnoughError(Exception):
    def __init__(self, ticker: str, have: int, need: int):
        super(NotEnoughError, self).__init__()
        self.ticker = ticker
        self.need = need
        self.have = have


def buy_stock(portfolio_id: int, ticker: str, quantity: int):
    current_money = quantity_in_portfolio(portfolio_id, config.CURRENCY)
    current_price = price_int(ticker) * quantity
    if current_money >= current_price:
        transaction_storage.add_transaction_batch((
            Transaction(portfolio_id=portfolio_id, ticker=config.CURRENCY, quantity=-current_price),
            Transaction(portfolio_id=portfolio_id, ticker=ticker, quantity=quantity)
        ))
    else:
        raise NotEnoughError(config.CURRENCY, current_money, current_price)


def sell_stock(portfolio_id: int, ticker: str, quantity: int):
    current_quantity = quantity_in_portfolio(portfolio_id, ticker)
    current_price = price_int(ticker) * quantity
    if current_quantity >= quantity:
        transaction_storage.add_transaction_batch((
            Transaction(portfolio_id=portfolio_id, ticker=ticker, quantity=-quantity),
            Transaction(portfolio_id=portfolio_id, ticker=config.CURRENCY, quantity=current_price)
        ))
    else:
        raise NotEnoughError(ticker, current_quantity, quantity)


def add_stock(portfolio_id: int, ticker: str, quantity: int):
    transaction_storage.add_transaction_batch((
        Transaction(portfolio_id=portfolio_id, ticker=ticker, quantity=quantity),
    ))
