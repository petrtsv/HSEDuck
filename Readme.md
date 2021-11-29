# HSEDuck Bot
A university project on Python: a stock exchange simulator, functioning as a telegram bot.

Using this bot you can collect virtual investment portfolio with virtual money to buy virtual stocks for real market prices. 

You can test your investment strategy without spending real money!

## Usage
A deployed telegram bot is available: [@HSEDuckBot](https://t.me/hseduckbot). 

Bot is working on Heroku platform, with CD pipeline from GitHub repository (branch `master`): https://github.com/petrtsv/HSEDuck

Stock prices are updated every hour using `yfinance` library.

### Bot commands
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

## Manual deployment

To deploy the application on your own you have to:

1. Install dependencies: `pip install -r requirements.txt`
2. Set following environment variables
    * `HSEDUCK_TG_TOKEN` — telegram bot token
    * `HSEDUCK_DEBUG` — if you want to use sqlite database stored in a file in the app folder; otherwise, `DATABASE_URL` must be set to PostgreSQL connection string.
3. Run `python entrypoint.py`

Configuration is stored in `config.py`

## TODOs
1. Add short-selling
2. Show price change during lat day, week etc
3. Add portfolio deletion