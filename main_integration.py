from ai.signal_engine import AISignalEngine
from risk.risk_controls import RiskControls
from trading.stop_manager import StopManager


class TradingLoop:
    def __init__(self):
        self.ai = AISignalEngine()
        self.risk = RiskControls()
        self.stop = StopManager()

    def process(self, market_data):
        signal = self.ai.predict(market_data)
        return {
            'signal': signal,
            'protection': self.stop.calculate(
                market_data.get('price', 0),
                signal
            ) if signal in ['BUY', 'SELL'] else None
        }
