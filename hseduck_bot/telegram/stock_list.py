from telegram import Update
from telegram.ext import CallbackContext

from hseduck_bot.controller import stocks
from hseduck_bot.telegram.template_utils import get_text


def run(update: Update, context: CallbackContext):
    stock_list = stocks.all_stocks()
    for stock in stock_list:
        template_args = {
            'name': stock.name,
            'ticker': stock.ticker,
            'price': stocks.price_str(stock.ticker)
        }
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('stock_description_short', template_args),
                                 parse_mode='HTML',
                                 disable_notification=True)
