import os

# تنظیمات تلگرام
TELEGRAM_BOT_TOKEN = "8943566078:AAHqmGIlhnGbkz8b9AihUQHyrDZRaGKPVUU"
TELEGRAM_CHAT_ID = "75217818"
TRADING_MODE = os.getenv('TRADING_MODE', 'paper')
INITIAL_BALANCE = float(os.getenv('INITIAL_BALANCE', '10000'))

SYMBOLS = [
    "GBPUSD",
    "EURUSD",
    "USDJPY",
    "AUDUSD",
    "XAUUSD",
    
]