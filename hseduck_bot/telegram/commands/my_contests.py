import traceback

from telegram import Update
from telegram.ext import CallbackContext

from hseduck_bot.controller import users, contests
from hseduck_bot.telegram.template_utils import get_text
from hseduck_bot.telegram.views.contest_view import contest_view


def run(update: Update, context: CallbackContext):
    try:
        user = users.login(update.effective_user.username)
        user_contests = contests.list_contests_for_user_id(user.id)

        if len(user_contests) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=get_text('no_contests'), parse_mode='HTML')
            return

        for contest in user_contests:
            message_text = contest_view(contest, user_id=user.id)

            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=message_text, parse_mode='HTML', disable_notification=True)

    except Exception:
        print(traceback.format_exc())
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('error'), parse_mode='HTML')
