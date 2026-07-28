class BacktestEngine:
    def __init__(self, balance=10000):
        self.balance = balance
        self.trades = []

    def run(self, prices, strategy):
        for price in prices:
            signal = strategy(price)
            self.trades.append({
                'price': price,
                'signal': signal
            })
        return self.trades
