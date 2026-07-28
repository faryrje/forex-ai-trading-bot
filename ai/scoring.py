class AIScoringEngine:

    def calculate(self, data):

        score = 50

        rsi = data.get("rsi", 50)

        if rsi < 30:
            score += 20

        elif rsi > 70:
            score -= 20


        trend = data.get("ema_trend")

        if trend == "UP":
            score += 15

        elif trend == "DOWN":
            score -= 15


        if data.get("volume") == "HIGH":
            score += 10


        if score >= 70:
            signal = "BUY"

        elif score <= 30:
            signal = "SELL"

        else:
            signal = "HOLD"


        return {
            "signal": signal,
            "score": score
        }