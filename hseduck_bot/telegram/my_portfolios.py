from telegram import Update
from telegram.ext import CallbackContext

from hseduck_bot import config
from hseduck_bot.controller import users, portfolios, stocks, transactions
from hseduck_bot.model.stocks import StockInfo
from hseduck_bot.telegram.template_utils import get_text


def money_to_str(x):
    return config.PRICE_REPR % x


def run(update: Update, context: CallbackContext):
    try:
        user = users.login(update.effective_user.username)
        user_portfolios = portfolios.list_portfolios_for_user(user.id)

        if len(user_portfolios) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=get_text('no_portfolios'), parse_mode='HTML')
            return

        for portfolio in user_portfolios:
            money = money_to_str(0)
            elements = []
            portfolio_cost = 0
            for ticker in portfolios.get_tickers_for_portfolio(portfolio.id):
                quantity = transactions.quantity_in_portfolio(portfolio.id, ticker)
                price = stocks.price_float(ticker) if ticker != config.CURRENCY else 1. / config.PRICE_PRECISION
                cost = price * quantity
                portfolio_cost += cost

                if ticker == config.CURRENCY:
                    money = money_to_str(cost)
                    continue

                stock_info: StockInfo = stocks.get_info(ticker)

                elements.append(get_text('portfolio_element', {
                    'name': stock_info.name,
                    'quantity': quantity,
                    'cost': money_to_str(cost)
                }))

            message_text = get_text('portfolio_description', {
                'name': portfolio.name,
                'id': portfolio.id,
                'current_cost': money_to_str(portfolio_cost),
                'usd': money_to_str(money),
                'elements': '\n\n'.join(elements)
            })

            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=message_text, parse_mode='HTML', disable_notification=True)

    except Exception as e:
        print(e)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('error'), parse_mode='HTML')
