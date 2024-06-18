import os
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
# if not all([BASE_URL, API_KEY, API_SECRET]):
#     raise ValueError("One or more environment variables are missing!")

# print(f"BASE_URL: {BASE_URL}")
# print(f"API_KEY: {API_KEY}")
# print(f"API_SECRET: {API_SECRET}")

ALPACA_CREDS={
    "API_KEY": os.getenv("API_KEY"),
    "API_SECRET": os.getenv("API_SECRET"),
    "PAPER": True,
}

# Define the strategy

symbol="SPY"

class MyStrategy(Strategy):
    def initialize(self,symbol):
        self.symbol = symbol
        self.sleep_time = "24H"
        self.last_trade = None
    def trading(self):
        if self.last_trade == None:
            order = self.create_order(
                self.symbol,
                10,
                "buy",
                type="market",
            )
            self.submit_order(order)
            self.last_trade = "buy"   
    
        
startdate=datetime(2023,12,15)
enddate=datetime(2023,12,31)

broker=Alpaca(ALPACA_CREDS)

strategy=MyStrategy(
    name="MyStrategy",
    broker=broker,
    parameters={"symbol":symbol})

strategy.backtest(
    YahooDataBacktesting,
    startdate,
    enddate,
    parameters={"symbol":symbol},
    )