import time
import logging
from config import INITIAL_BALANCE, SYMBOLS, TRADING_MODE
from risk.manager import RiskManager
from strategy.engine import StrategyEngine

logging.basicConfig(level=logging.INFO)


def run_bot():
    logging.info('Forex AI Trading Bot started')
    logging.info('Mode: %s', TRADING_MODE)

    risk = RiskManager(INITIAL_BALANCE)
    strategy = StrategyEngine()

    while True:
        try:
            for symbol in SYMBOLS:
                signal = strategy.analyze(symbol)
                logging.info('%s signal: %s', symbol, signal)

            time.sleep(10)
        except Exception:
            logging.exception('Trading loop error')
            time.sleep(30)


if __name__ == '__main__':
    run_bot()
