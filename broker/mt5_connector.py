class MT5Connector:
    def __init__(self):
        self.connected = False

    def connect(self):
        # TODO: initialize MetaTrader5 package
        self.connected = True
        return self.connected

    def get_price(self, symbol):
        if not self.connected:
            raise RuntimeError('MT5 is not connected')

        # TODO: replace with real tick data
        return None

    def send_order(self, order):
        if not self.connected:
            raise RuntimeError('MT5 is not connected')

        # TODO: real MT5 order execution
        return {'status': 'paper', 'order': order}
