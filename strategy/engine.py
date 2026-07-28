from ai.signal_engine import AISignalEngine

class StrategyEngine:
    def __init__(self):
        self.ai_engine = AISignalEngine()

    def analyze(self, market_data):
        signal = self.ai_engine.predict(market_data)
        return signal