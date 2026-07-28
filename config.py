import os

TRADING_MODE = os.getenv('TRADING_MODE', 'paper')
INITIAL_BALANCE = float(os.getenv('INITIAL_BALANCE', '10000'))

SYMBOLS = [
    'EURUSD',
    'GBPUSD',
    'XAUUSD'
]
