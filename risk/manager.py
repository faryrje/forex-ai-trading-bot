class RiskManager:
    def __init__(self, balance):
        self.balance = balance
        self.max_daily_loss = balance * 0.02

    def can_trade(self):
        return True
