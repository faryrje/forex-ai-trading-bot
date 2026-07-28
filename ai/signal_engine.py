class AISignalEngine:
    def predict(self, market_data):
        rsi = market_data.get('rsi')
        price = market_data.get('close')
        ema_200 = market_data.get('ema_200')

        if rsi is None or price is None or ema_200 is None:
            return 'HOLD'

        # استفاده از یک فیلتر متعادل‌تر (به جای سخت‌گیری مطلق قبلی)
        # خرید در RSI پایین وقتی خیلی از EMA 200 دور نشده یا روند کلی صعودی است
        if rsi < 38 and price >= (ema_200 * 0.98):
            return 'BUY'
        
        # فروش در RSI بالا وقتی خیلی از EMA 200 پایین‌تر نیامده
        if rsi > 62 and price <= (ema_200 * 1.02):
            return 'SELL'

        return 'HOLD'