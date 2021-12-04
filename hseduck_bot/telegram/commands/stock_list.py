from telegram import Update
from telegram.ext import CallbackContext

from hseduck_bot.controller import stocks
from hseduck_bot.telegram.template_utils import get_text

MESSAGE_LEN_LIMIT = 3000


def run(update: Update, context: CallbackContext):
    stock_list = stocks.all_stocks()
    stock_info_strings = []
    cur_ln = 0
    for stock in stock_list:
        template_args = {
            'name': stock.name,
            'ticker': stock.ticker,
            'price': stocks.price_str(stock.ticker)
        }
        cur_info = get_text('stock_description_short', template_args)
        if cur_ln + len(cur_info) > MESSAGE_LEN_LIMIT:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="\n\n".join(stock_info_strings),
                                     parse_mode='HTML',
                                     disable_notification=True)
            stock_info_strings = []
            cur_ln = 0

        stock_info_strings.append(cur_info)
        cur_ln += len(cur_info)

    if cur_ln > 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="\n\n".join(stock_info_strings),
                                 parse_mode='HTML',
                                 disable_notification=True)
