class MarketDataLoader:
    def __init__(self):
        self.prices = {}

    def add_tick(self, symbol, price):
        self.prices.setdefault(symbol, []).append(price)

    def get_prices(self, symbol):
        return self.prices.get(symbol, [])
