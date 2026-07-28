def calculate_metrics(trades):
    profits = [t.get('profit', 0) for t in trades]
    total = len(profits)
    wins = [p for p in profits if p > 0]
    losses = [p for p in profits if p < 0]

    gross_profit = sum(wins)
    gross_loss = abs(sum(losses))

    return {
        'trades': total,
        'win_rate': round((len(wins) / total * 100), 2) if total else 0,
        'profit_factor': round(gross_profit / gross_loss, 2) if gross_loss else None,
        'net_profit': round(sum(profits), 2)
    }
