import logging
import time
import MetaTrader5 as mt5
from config import SYMBOLS
from core.trading_engine import TradingEngine

# تنظیمات لاگینگ برای نمایش بهتر
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    logging.info("Forex AI Trading Bot starting...")

    # ۱. اتصال به متاتریدر ۵
    if not mt5.initialize():
        logging.error("Failed to initialize MetaTrader 5")
        return

    logging.info("Successfully connected to MetaTrader 5")

    # ۲. ساخت نمونه از موتور معامله‌گر
    engine = TradingEngine(symbols=SYMBOLS)

    logging.info("Bot is running in continuous loop. Press Ctrl+C to stop.\n")

    try:
        while True:
            # دریافت داده‌های اسکن شده از تمام نمادها
            market_data = engine.scanner.analyze()

            # نمایش وضعیت زنده نمادها در ترمینال
            print("-" * 65)
            print(f"🔍 SCANNING MARKET ({len(market_data)} Symbols)...")
            for item in market_data:
                symbol = item.get("symbol")
                price = item.get("price")
                rsi = item.get("rsi")
                atr = item.get("atr")
                
                # تبدیل ATR به پیپ جهت خوانایی بهتر
                pip_size = 0.01 if "JPY" in symbol or "XAU" in symbol else 0.0001
                atr_pips = round(atr / pip_size, 1) if atr else 0

                print(
                    f"🔹 {symbol:<7} | Price: {price:<8.5f} | "
                    f"RSI: {rsi:<5.1f} | ATR: {atr_pips:>4.1f} pips"
                )
            print("-" * 65)

            # اجرای چرخه تصمیم‌گیری
            # تبدیل دیتا به فرمت dict برای موتور trading_engine
            data_dict = {item["symbol"]: item for item in market_data}
            result = engine.run_cycle(data_dict)
            
            logging.info("Cycle Result: %s\n", result)

            # وقفه ۱۵ ثانیه‌ای تا چرخه بعدی
            time.sleep(15)

    except KeyboardInterrupt:
        logging.info("Bot stopped manually by user.")
    finally:
        mt5.shutdown()
        logging.info("MetaTrader 5 connection closed.")


if __name__ == "__main__":
    main()