from telegram import Update
from telegram.ext import CallbackContext

from hseduck_bot.telegram.template_utils import get_text


def run(update: Update, context: CallbackContext):
    name = update.effective_user.first_name
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_text('start', {'name': name}),
                             parse_mode='HTML')
