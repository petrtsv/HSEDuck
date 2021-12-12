# HSEDuck Bot

A university project on Python: a stock exchange simulator, functioning as a telegram bot.

Using this bot you can collect virtual investment portfolio with virtual money to buy virtual stocks for real market
prices.

You can test your investment strategy without spending real money!

## Usage

A deployed telegram bot is available: [@HSEDuckBot](https://t.me/hseduckbot).

Bot is working on Heroku platform, with CD pipeline from GitHub repository (
branch `master`): https://github.com/petrtsv/HSEDuck

Stock prices are updated every hour using `yfinance` library.

### Basic bot commands

`/help` — prints help message

`/stock_list` — prints all available stocks

`/my_portfolios` — prints list of all your portfolios

`/new_portfolio NAME` — creates a new portfolio with initial balance of `$10'000`

`/buy PORTFOLIO_ID TICKER QUANTITY` — buys some stock for one of your portfolios

`/sell PORTFOLIO_ID TICKER QUANTITY` — sells some stock from one of your portfolios

### Example

Create investment portfolio; buy 3 FB stocks and sell one of them:

1. `/new_portfolio Foo`
2. `/my_portfolios` — find Foo portfolio and remember its ID
3. `/buy ID FB 3`
4. `/my_portfolios` — to see the result
5. `/sell ID FB 1`
6. `/my_portfolios` — to see the result again

### Competitive mode

The bot has an option for creating _contests_. After joining a contest, user receives a special portfolio, connected to
it.

The total cost of this portfolio is your result: you can see a leaderboard, containing results of all users, joined the
same contest.

When creating a contest, owner chooses name and duration: after given amount of hours it is forbidden to perform any
operation on connected portfolios.

Here are the commands for the competitive mode:

`/new_contest NAME HOURS` — creates a new contest with given name (note: name can only be _one word_), lasting for the
given amount of hours

`/my_contests` — prints full information about all contests you have joined

`/join CONTEST_ID` — join the contest with given id

`/join global` — join an eternal global competition

_NOTE: actual results will be displayed only after all short positions will be automatically covered (maximum 24 hours after the end of the contest)._ 

### Short-selling

This bot also supports _short-selling_. You can borrow some stocks from the virtual broker for 24 hours. Stocks are
immediately sold and money is transferred to the portfolio. After deadline, stocks are automatically taken from the
portfolio (and purchased, if the amount is not enough to cover the short position).

_After deadline, you can get negative amount of money on your portfolio._

There's a limitation on short-selling: you cannot borrow stocks if total cost of not covered short position
exceeds `$10'000` after the requested operation.

Command to open a short position works similar to buy/sell commands:

`/short PORTFOLIO_ID TICKER QUANTITY`

## Manual deployment

To deploy the application on your own you have to:

1. Install dependencies: `pip install -r requirements.txt`
2. Set following environment variables
    * `HSEDUCK_TG_TOKEN` — telegram bot token
    * `HSEDUCK_DEBUG` — if you want to use sqlite database stored in a file in the app folder; otherwise, `DATABASE_URL`
      must be set to PostgreSQL connection string.
3. Run `python entrypoint.py`

Configuration is stored in `config.py`
