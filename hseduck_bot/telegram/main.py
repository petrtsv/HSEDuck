from telegram.ext import Updater, Dispatcher, CommandHandler

from hseduck_bot import config
from hseduck_bot.controller.lifecycle import load, unload
from hseduck_bot.telegram.commands import buy, help_command, new_contest, stock_list, sell, my_portfolios, \
    new_portfolio, start, my_contests, join_contest, short
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

        new_contest_handler = CommandHandler('new_contest', new_contest.run)
        dispatcher.add_handler(new_contest_handler)

        my_contests_handler = CommandHandler('my_contests', my_contests.run)
        dispatcher.add_handler(my_contests_handler)

        join_contest_handler = CommandHandler('join_contest', join_contest.run)
        dispatcher.add_handler(join_contest_handler)

        short_handler = CommandHandler('short', short.run)
        dispatcher.add_handler(short_handler)

        updater.start_polling()

        await async_idle()
    finally:
        await unload()
