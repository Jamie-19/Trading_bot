import os
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv('BASE_URL')
ALPACA_CREDS={
    "API_KEY": os.getenv('API_KEY'),
    "API_SECRET": os.getenv('API_SECRET'),
    "PAPER": True,
}

class TradingBot(Strategy):
    def initialize(self):



broker=Alpaca(ALPACA_CREDS)
