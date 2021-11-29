import traceback

from telegram import Update
from telegram.ext import CallbackContext

from hseduck_bot.controller import portfolios, users, stocks, transactions
from hseduck_bot.controller.transactions import NotEnoughError
from hseduck_bot.telegram.template_utils import get_text

MAX_NAME_LENGTH = 100


def run(update: Update, context: CallbackContext):
    text = update.message.text
    args = text.split()

    if len(args) != 4:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('input_validation.missing_arguments', {'arguments': 'some'}),
                                 parse_mode='HTML')
        return

    try:
        portfolio_id: int = int(args[1])
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('input_validation.invalid_arguments', {'arguments': 'PORTFOLIO_ID'}),
                                 parse_mode='HTML')
        return

    ticker = args[2]

    try:
        quantity: int = int(args[3])
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('input_validation.invalid_arguments', {'arguments': 'QUANTITY'}),
                                 parse_mode='HTML')
        return

    if quantity <= 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('input_validation.invalid_arguments', {'arguments': 'QUANTITY'}),
                                 parse_mode='HTML')
        return

    try:
        ticker_info = stocks.get_info(ticker)
        if ticker_info is None:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=get_text('input_validation.invalid_arguments', {'arguments': 'TICKER'}),
                                     parse_mode='HTML')
            return

        portfolio = portfolios.get_by_id(portfolio_id)
        user = users.login(update.effective_user.username)
        if portfolio is None or portfolio.owner_id != user.id:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=get_text('input_validation.invalid_arguments', {'arguments': 'PORTFOLIO_ID'}),
                                     parse_mode='HTML')
            return

        try:
            transactions.sell_stock(portfolio_id, ticker, quantity)
        except NotEnoughError:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=get_text('no_items'),
                                     parse_mode='HTML')
            return

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('done'), parse_mode='HTML')
    except Exception:
        print(traceback.format_exc())
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('error'), parse_mode='HTML')
