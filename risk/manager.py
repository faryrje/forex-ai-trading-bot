class RiskManager:
    def __init__(self, balance, max_daily_loss_pct=0.02):
        self.initial_daily_balance = balance
        self.current_balance = balance
        self.max_daily_loss = balance * max_daily_loss_pct

    def update_balance(self, current_balance):
        self.current_balance = current_balance

    def can_trade(self):
        current_loss = self.initial_daily_balance - self.current_balance
        if current_loss >= self.max_daily_loss:
            return False
        return True