from typing import Optional

from hseduck_bot import config
from hseduck_bot.controller import portfolios, transactions, stocks, contests
from hseduck_bot.model.portfolios import Portfolio
from hseduck_bot.model.stocks import StockInfo
from hseduck_bot.telegram.commands.utils import money_to_str
from hseduck_bot.telegram.template_utils import get_text
from hseduck_bot.telegram.views.contest_view import status_view


def portfolio_view(portfolio: Portfolio, user_id: Optional[int] = None):
    money = money_to_str(0)
    elements = []
    portfolio_cost = 0
    for ticker in portfolios.get_tickers_for_portfolio(portfolio.id):
        cost, quantity = transactions.cost_in_portfolio(portfolio.id, ticker, with_quantity=True)
        portfolio_cost += cost

        if ticker == config.CURRENCY:
            money = money_to_str(cost)
            continue

        stock_info: StockInfo = stocks.get_info(ticker)

        elements.append(get_text('portfolio_element', {
            'name': stock_info.name,
            'ticker': stock_info.ticker,
            'quantity': quantity,
            'cost': money_to_str(cost)
        }))
    if portfolio.contest_id is None:
        portfolio_text = get_text('portfolio_description', {
            'name': portfolio.name,
            'id': portfolio.id,
            'current_cost': money_to_str(portfolio_cost),
            'usd': money,
            'elements': '\n\n'.join(elements)
        })
    else:
        if user_id is None:
            raise ValueError('Cannot print contest info: user_id is None')
        contest = contests.get_by_id(portfolio.contest_id)
        result = contests.get_contest_result_by_user_id(contest_id=contest.id, user_id=user_id)
        portfolio_text = get_text('portfolio_description_contest', {
            'contest_name': contest.name,
            'contest_id': contest.id,
            'contest_status': status_view(contest.status),
            'portfolio_id': portfolio.id,
            'current_cost': money_to_str(result[1]),
            'place': result[0] + 1,
            'usd': money,
            'elements': '\n\n'.join(elements)
        })

    return portfolio_text
