import logging

from scanner.market_scanner import MarketScanner
from ai.scoring import AIScoringEngine
from trading.paper_account import PaperAccount
from risk.risk_controls import RiskControls


class TradingEngine:

    def __init__(self, symbols):
        self.scanner = MarketScanner(symbols)
        self.ai = AIScoringEngine()
        self.account = PaperAccount(10000)
        self.risk = RiskControls()

    def run_cycle(self, market_data):

        opportunities = self.scanner.analyze(
            market_data
        )

        if not opportunities:
            return {
                "status": "NO_SIGNAL"
            }

        best = opportunities[0]

        decision = self.ai.calculate({
            "rsi": best["rsi"],
            "ema_trend": best["trend"],
            "volume": "HIGH"
        })

        logging.info(
            "%s %s %s",
            best["symbol"],
            decision["signal"],
            decision["score"]
        )

        if decision["signal"] == "BUY":

            if self.risk.allow_trade(
                self.account.balance
            ):

                return self.account.open_trade(
                    best["symbol"],
                    "BUY",
                    0.01,
                    best["price"]
                )

        return decision