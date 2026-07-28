class RiskControls:
    def __init__(self, max_daily_loss_percent=2):
        self.max_daily_loss_percent = max_daily_loss_percent
        self.daily_loss = 0

    def allow_trade(self, balance):
        limit = balance * self.max_daily_loss_percent / 100
        return self.daily_loss < limit

    def register_loss(self, amount):
        self.daily_loss += abs(amount)
