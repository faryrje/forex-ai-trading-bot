def calculate_position_size(balance, risk_percent, stop_loss_pips, pip_value_per_lot=10):
    if stop_loss_pips <= 0:
        return 0.0

    risk_amount = balance * (risk_percent / 100)
    lot_size = risk_amount / (stop_loss_pips * pip_value_per_lot)
    return max(0.01, round(lot_size, 2))