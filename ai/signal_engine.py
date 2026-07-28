class AISignalEngine:
    def predict(self, market_data):
        rsi = market_data.get('rsi')

        if rsi is None:
            return 'HOLD'

        if rsi < 30:
            return 'BUY'
        if rsi > 70:
            return 'SELL'

        return 'HOLD'
