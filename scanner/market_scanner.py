import logging
import MetaTrader5 as mt5
import pandas as pd


class MarketScanner:

    def __init__(self, symbols, timeframe=mt5.TIMEFRAME_M15):
        self.symbols = symbols
        self.timeframe = timeframe

    def _calculate_atr(self, df, period=14):
        """محاسبه اندیکاتور ATR بر اساس کندل‌های قیمتی"""
        if len(df) < period + 1:
            return 0.0015  # مقدار پیش‌فرض در صورت عدم وجود داده کافی

        high = df['high']
        low = df['low']
        close = df['close']

        # محاسبه True Range (TR)
        tr1 = high - low
        tr2 = (high - close.shift(1)).abs()
        tr3 = (low - close.shift(1)).abs()

        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # محاسبه میانگین متحرک TR (همان ATR)
        atr = tr.rolling(window=period).mean()
        return atr.iloc[-1]

    def _calculate_rsi(self, series, period=14):
        """محاسبه اندیکاتور RSI"""
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]

    def analyze(self, market_data=None):
        """اسکن بازار و استخراج RSI, EMA_200 و ATR"""
        results = []

        for symbol in self.symbols:
            # دریافت ۱۰۰ کندل اخیر از MT5
            rates = mt5.copy_rates_from_pos(symbol, self.timeframe, 0, 100)
            if rates is None or len(rates) == 0:
                logging.warning(f"Failed to fetch rate data for {symbol}")
                continue

            df = pd.DataFrame(rates)
            current_price = df['close'].iloc[-1]

            # محاسبه اندیکاتورها
            rsi_val = self._calculate_rsi(df['close'], period=14)
            ema_200_val = df['close'].ewm(span=200, adjust=False).mean().iloc[-1]
            atr_val = self._calculate_atr(df, period=14)

            results.append({
                "symbol": symbol,
                "price": current_price,
                "rsi": rsi_val,
                "ema_200": ema_200_val,
                "atr": atr_val,  # 👈 مقدار ATR اضافه شد
            })

        return results