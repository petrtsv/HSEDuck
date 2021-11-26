from typing import Optional

from hseduck_bot import config
from hseduck_bot.controller.stocks import price
from hseduck_bot.model.transactions import TransactionStorage, Transaction

transaction_storage: Optional[TransactionStorage] = None


def initialize(storage: TransactionStorage):
    global transaction_storage
    transaction_storage = storage


def quantity_in_portfolio(portfolio_id: int, ticker: str):
    return transaction_storage.get_quantity(portfolio_id, ticker)


def buy_stock(portfolio_id: int, ticker: str, quantity: int):
    current_money = quantity_in_portfolio(portfolio_id, config.CURRENCY)
    current_price = price(ticker) * quantity
    if current_money >= current_price:
        transaction_storage.add_transaction_batch((
            Transaction(portfolio_id=portfolio_id, ticker=config.CURRENCY, quantity=-current_price),
            Transaction(portfolio_id=portfolio_id, ticker=ticker, quantity=quantity)
        ))


def sell_stock(portfolio_id: int, ticker: str, quantity: int):
    current_quantity = quantity_in_portfolio(portfolio_id, ticker)
    current_price = price(ticker) * quantity
    if current_quantity >= quantity:
        transaction_storage.add_transaction_batch((
            Transaction(portfolio_id=portfolio_id, ticker=ticker, quantity=-quantity),
            Transaction(portfolio_id=portfolio_id, ticker=config.CURRENCY, quantity=current_price)
        ))
