import datetime
import re
import traceback

from telegram import Update
from telegram.ext import CallbackContext

from hseduck_bot.controller import users, contests
from hseduck_bot.telegram.template_utils import get_text, wrong_format_message
from hseduck_bot.telegram.views.contest_view import contest_view

NAME_REGEX = re.compile(r'^/\S+\s+(.+?)\s*$')
MAX_NAME_LENGTH = 100


def run(update: Update, context: CallbackContext):
    text = update.message.text
    tokens = text.strip().split()
    if '\n' in text or len(tokens) != 3:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=wrong_format_message("new_contest"),
                                 parse_mode='HTML')
        return
    name = tokens[1]
    if len(name) > MAX_NAME_LENGTH:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('input_validation.too_long', {'argument': 'NAME'}), parse_mode='HTML')
        return
    try:
        hours = int(tokens[2])
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('input_validation.invalid_arguments', {"arguments": "HOURS"}),
                                 parse_mode='HTML')
        return

    try:
        user = users.login(update.effective_user.username)

        now = datetime.datetime.now()
        delta = datetime.timedelta(hours=hours)
        new_contest = contests.create_contest(user_id=user.id, name=name, start_date=now, end_date=now + delta)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=contest_view(new_contest, user_id=user.id), parse_mode='HTML')
    except Exception:
        print(traceback.format_exc())
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('error'), parse_mode='HTML')
