from telegram.ext import Updater, Dispatcher, CommandHandler

from hseduck_bot import config
from hseduck_bot.controller.lifecycle import load, unload
from hseduck_bot.telegram import start, stock_list, help_command, new_portfolio, my_portfolios, buy, sell
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

        new_portfolio_handler = CommandHandler('new_portfolio', new_portfolio.run)
        dispatcher.add_handler(new_portfolio_handler)

        my_portfolios_handler = CommandHandler('my_portfolios', my_portfolios.run)
        dispatcher.add_handler(my_portfolios_handler)

        buy_handler = CommandHandler('buy', buy.run)
        dispatcher.add_handler(buy_handler)

        sell_handler = CommandHandler('sell', sell.run)
        dispatcher.add_handler(sell_handler)

        updater.start_polling()

        await async_idle()
    finally:
        await unload()
