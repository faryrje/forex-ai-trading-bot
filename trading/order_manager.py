class OrderManager:
    def __init__(self, broker, risk_manager):
        self.broker = broker
        self.risk_manager = risk_manager

    def open_trade(self, symbol, side, volume, stop_loss, take_profit):
        if not self.risk_manager.can_trade():
            return None

        order = {
            'symbol': symbol,
            'side': side,
            'volume': volume,
            'stop_loss': stop_loss,
            'take_profit': take_profit
        }

        return self.broker.send_order(order)
