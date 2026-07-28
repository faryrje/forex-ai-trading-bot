def calculate_position_size(balance, risk_percent, stop_loss_distance):
    if stop_loss_distance <= 0:
        return 0

    risk_amount = balance * (risk_percent / 100)
    return risk_amount / stop_loss_distance
