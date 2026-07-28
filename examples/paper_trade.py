from strategy.engine import StrategyEngine

engine = StrategyEngine()

# نمونه دیتای تست ورودی
test_market_data = {
    'rsi': 25,
    'close': 1.0850,
    'ema_200': 1.0800
}

# خروجی باید BUY بشه (چون RSI زیر 30 و قیمت بالای EMA200 هست)
signal = engine.analyze(test_market_data)
print(f"Signal Result: {signal}")