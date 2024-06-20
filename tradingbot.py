import os
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Environment variables
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# if not all([BASE_URL, API_KEY, API_SECRET]):
#     raise ValueError("One or more environment variables are missing!")

# # Print statements for debugging
# print(f"BASE_URL: {BASE_URL}")
# print(f"API_KEY: {API_KEY}")
# print(f"API_SECRET: {API_SECRET}")

# Alpaca credentials
ALPACA_CREDS = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True,
}

symbol = "AAPL"
# Define the strategy
class MyStrategy(Strategy):
    def initialize(self,symbol):
        self.symbol = symbol
        self.sleep_time = "24H"
        self.last_trade = None

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)


    def on_trading_iteration(self):
        if self.last_trade == None:
            order = self.create_order(
                self.symbol,
                10,
                "buy",
                type="market",
            )
            self.submit_order(order)
            self.last_trade = "buy"

# Backtest dates
start_date = datetime(2023, 12, 15)
end_date = datetime(2023, 12, 31)

# Broker setup
broker = Alpaca(ALPACA_CREDS)

# Strategy setup
strategy = MyStrategy(
    name="MLStrat",
    broker=broker,
    parameters={"symbol": symbol}
)

# Run the backtest
strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={"symbol": symbol},
)
