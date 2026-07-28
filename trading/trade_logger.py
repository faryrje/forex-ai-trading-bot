import json
from datetime import datetime


class TradeLogger:

    def __init__(self, file="trades.json"):
        self.file = file


    def save(self, trade):

        trade["time"] = str(
            datetime.now()
        )

        try:
            with open(
                self.file,
                "r"
            ) as f:
                trades = json.load(f)

        except:
            trades = []


        trades.append(trade)


        with open(
            self.file,
            "w"
        ) as f:
            json.dump(
                trades,
                f,
                indent=4
            )