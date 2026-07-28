from indicators.technical import rsi, ema


class MarketScanner:

    def __init__(self, symbols):
        self.symbols = symbols


    def analyze(self, market):

        results = []

        for symbol in self.symbols:

            prices = market.get(symbol, [])

            if len(prices) < 5:
                continue

            rsi_value = rsi(prices)
            ema_value = ema(prices)

            score = 0

            if rsi_value < 30:
                score += 30

            elif rsi_value > 70:
                score -= 30


            trend = (
                "UP"
                if prices[-1] > ema_value
                else "DOWN"
            )

            if trend == "UP":
                score += 20
            else:
                score -= 20


            results.append({
                "symbol": symbol,
                "price": prices[-1],
                "rsi": rsi_value,
                "trend": trend,
                "score": score
            })


        return sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )