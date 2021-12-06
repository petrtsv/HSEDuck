import traceback

from telegram import Update
from telegram.ext import CallbackContext

from hseduck_bot.controller import portfolios, users, stocks, transactions, contests
from hseduck_bot.controller.transactions import NotEnoughError
from hseduck_bot.telegram.template_utils import get_text
from hseduck_bot.telegram.views.contest_view import contest_view


def run(update: Update, context: CallbackContext):
    text = update.message.text
    args = text.split()

    if len(args) != 2:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('input_validation.invalid.format'),
                                 parse_mode='HTML')
        return

    try:
        contest_id: int = int(args[1])
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('input_validation.invalid_arguments', {'arguments': 'CONTEST_ID'}),
                                 parse_mode='HTML')
        return

    try:
        contest = contests.get_by_id(contest_id)
        if contest is None:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=get_text('input_validation.invalid_arguments', {'arguments': 'CONTEST_ID'}),
                                     parse_mode='HTML')
            return

        user = users.login(update.effective_user.username)
        if contests.is_participant(user.id, contest.id):
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=get_text('input_validation.already_joined'),
                                     parse_mode='HTML')
            return
        contests.join_contest(user.id, contest.id)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=contest_view(contest, user_id=user.id), parse_mode='HTML')
    except Exception:
        print(traceback.format_exc())
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=get_text('error'), parse_mode='HTML')