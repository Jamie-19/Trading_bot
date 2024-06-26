import os
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from datetime import datetime
from dotenv import load_dotenv
from alpaca_trade_api import REST
from timedelta import Timedelta
from finbert_utils import estimate_sentiment

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
cash_at_risk = 0.5
# Define the strategy
class MyStrategy(Strategy):
    def initialize(self, symbol, cash_at_risk): 
        self.symbol = symbol
        self.sleeptime = "24H" 
        self.last_trade = None 
        # print("First trade: ", self.last_trade)
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)

    def position_sizing(self): 
        cash = self.get_cash() 
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price,0)
        return cash, last_price, quantity

    def get_dates(self): 
        today = self.get_datetime()
        prior = today - Timedelta(days=3)
        return today.strftime('%Y-%m-%d'), prior.strftime('%Y-%m-%d')

    def get_sentiment(self): 
        today, prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, 
                                 start=prior, 
                                 end=today) 
        news = [n.__dict__["_raw"]["headline"] for n in news]
        probability, sentiment = estimate_sentiment(news)
        return probability, sentiment 

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing() 
        probability, sentiment = self.get_sentiment()
        # print(f"Probability: {probability}, Sentiment: {sentiment}")

        if cash > last_price: 
            if sentiment == "positive" and probability > .999: 
                if self.last_trade == "sell": 
                    self.sell_all() 
                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    "buy", 
                    type="bracket", 
                    take_profit_price=last_price*1.20, 
                    stop_loss_price=last_price*.95
                )
                self.submit_order(order) 
                self.last_trade = "buy"
            elif sentiment == "negative" and probability > .999: 
                if self.last_trade == "buy": 
                    self.sell_all() 
                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    "sell", 
                    type="bracket", 
                    take_profit_price=last_price*.8, 
                    stop_loss_price=last_price*1.05
                )
                self.submit_order(order) 
                self.last_trade = "sell"


start_date = datetime(2023,1,1)
end_date = datetime(2023,12,31)


broker = Alpaca(ALPACA_CREDS) 

strategy = MyStrategy(name='mlstrat', broker=broker, 
                    parameters={"symbol":symbol, 
                                "cash_at_risk":cash_at_risk})

strategy.backtest(
    YahooDataBacktesting, 
    start_date, 
    end_date, 
    parameters={"symbol":symbol, "cash_at_risk":cash_at_risk}
)
