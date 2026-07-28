class StopManager:
    def calculate(self, entry, side, stop_percent=1, take_percent=2):
        if side == 'BUY':
            return {
                'stop_loss': entry * (1 - stop_percent / 100),
                'take_profit': entry * (1 + take_percent / 100)
            }

        return {
            'stop_loss': entry * (1 + stop_percent / 100),
            'take_profit': entry * (1 - take_percent / 100)
        }
