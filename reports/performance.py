def calculate_report(trades):
    total = len(trades)
    wins = [t for t in trades if t.get('profit', 0) > 0]

    win_rate = (len(wins) / total * 100) if total else 0

    return {
        'trades': total,
        'wins': len(wins),
        'win_rate': round(win_rate, 2)
    }
