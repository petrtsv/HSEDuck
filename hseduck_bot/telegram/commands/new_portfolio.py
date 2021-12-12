import re
import traceback

from telegram import Update
from telegram.ext import CallbackContext

from hseduck_bot.controller import portfolios, users
from hseduck_bot.telegram.template_utils import get_text, wrong_format_message

NAME_REGEX = re.compile(r'^/\S+\s+(.+?)\s*$')
MAX_NAME_LENGTH = 100


def run(update: Update, context: CallbackContext):
    text = update.message.text
    name_match = re.search(NAME_REGEX, text)
    if name_match is None:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=wrong_format_message("new_portfolio"),
                                 parse_mode='HTML')
        return
    name = name_match.group(1).strip()
    if '\n' in name:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('input_validation.one_row_only', {'argument': 'NAME'}),
                                 parse_mode='HTML')
        return
    if len(name) > MAX_NAME_LENGTH:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('input_validation.too_long', {'argument': 'NAME'}), parse_mode='HTML')
        return

    try:
        user = users.login(update.effective_user.username)
        portfolios.create_portfolio(user.id, name)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('done'), parse_mode='HTML')
    except Exception:
        print(traceback.format_exc())
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('error'), parse_mode='HTML')
