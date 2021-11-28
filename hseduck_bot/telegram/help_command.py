from telegram import Update
from telegram.ext import CallbackContext

from hseduck_bot.telegram.template_utils import get_text


def run(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_text('help'), parse_mode='HTML')
