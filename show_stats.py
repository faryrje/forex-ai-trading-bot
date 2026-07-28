from database import TradeDatabase


def main():
    db = TradeDatabase()
    stats = db.get_stats()

    print("=" * 45)
    print("      📊 FOREX AI TRADING BOT STATS REPORT    ")
    print("=" * 45)
    print(f"🔹 Total Closed Trades : {stats['total_trades']}")
    print(f"✅ Winning Trades      : {stats['winning_trades']}")
    print(f"❌ Losing Trades       : {stats['losing_trades']}")
    print(f"🎯 Win Rate            : {stats['win_rate']:.2f}%")
    print(f"💰 Total Profit/Loss   : ${stats['total_profit']:+.2f}")
    print("=" * 45)


if __name__ == "__main__":
    main()