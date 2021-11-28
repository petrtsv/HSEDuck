import asyncio

from telegram.ext import Updater, Dispatcher, CommandHandler

from hseduck_bot import config
from hseduck_bot.controller.lifecycle import load, unload
from hseduck_bot.telegram import start, stock_list, help_command
from hseduck_bot.util import async_idle


async def run_bot():
    await load()
    try:
        updater = Updater(token=config.TG_TOKEN)
        dispatcher: Dispatcher = updater.dispatcher

        start_handler = CommandHandler('start', start.run)
        dispatcher.add_handler(start_handler)

        help_handler = CommandHandler('help', help_command.run)
        dispatcher.add_handler(help_handler)

        all_stocks_handler = CommandHandler('stock_list', stock_list.run)
        dispatcher.add_handler(all_stocks_handler)

        updater.start_polling()

        await async_idle()
    finally:
        await unload()
