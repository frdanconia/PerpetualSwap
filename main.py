import requests
import random

class PerpetualSwap:
    def __init__(self, underlying_asset, leverage, position_size, maker_fee, taker_fee, moving_average_window):
        self.underlying_asset = underlying_asset
        self.leverage = leverage
        self.position_size = position_size
        self.maker_fee = maker_fee
        self.taker_fee = taker_fee
        self.moving_average_window = moving_average_window
        self.underlying_price = self.get_current_price()
        self.prices = []
        self.moving_average = None
        self.order_book = {"bids": [], "asks": []}
        
    def get_current_price(self):
        url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={self.underlying_asset}"
        headers = {
            "Accepts": "application/json",
            "X-CMC_Pro_API_Key": "your_api_key_here"
        }

        response = requests.get(url, headers=headers)
        data = response.json()
        return data["data"][self.underlying_asset]["quote"]["USD"]["price"]
    
    def calculate_margin(self):
        margin = self.position_size / self.leverage
        return margin
    
    def calculate_profit(self, new_price, is_maker):
        profit = (new_price - self.underlying_price) * self.position_size
        if is_maker:
            profit = profit - profit * (self.maker_fee / 100)
        else:
            profit = profit - profit * (self.taker_fee / 100)
        return profit
    
    def update_price(self):
        new_price = self.get_current_price()
        self.prices.append(new_price)
        if len(self.prices) > self.moving_average_window:
            self.prices.pop(0)
        self.moving_average = sum(self.prices) / len(self.prices)
        self.underlying_price = new_price
    
    def moving_average_strategy(self):
        if self.moving_average is None:
            return "Do not trade, not enough data"
        elif self.underlying_price > self.moving_average:
            return "Buy"
        else:
            return "Sell"
        
    def add_liquidity(self, price, volume, is_bid):
        if is_bid:
            self.order_book["bids"].append({"price": price, "volume": volume})
        else:
            self.order_book["asks"].append({"price": price, "volume": volume})