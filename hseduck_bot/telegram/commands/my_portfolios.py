import traceback

from telegram import Update
from telegram.ext import CallbackContext

from hseduck_bot.controller import users, portfolios
from hseduck_bot.telegram.template_utils import get_text
from hseduck_bot.telegram.views.portfolio_view import portfolio_view


def run(update: Update, context: CallbackContext):
    try:
        user = users.login(update.effective_user.username)
        user_portfolios = portfolios.list_portfolios_for_user(user.id)

        if len(user_portfolios) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=get_text('no_portfolios'), parse_mode='HTML')
            return

        for portfolio in user_portfolios:
            message_text = portfolio_view(portfolio, user_id=user.id)

            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=message_text, parse_mode='HTML', disable_notification=True)

    except Exception:
        print(traceback.format_exc())
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('error'), parse_mode='HTML')
