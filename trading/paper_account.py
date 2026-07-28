class PaperAccount:

    def __init__(self, balance=10000):

        self.balance = balance
        self.positions = []


    def open_trade(
        self,
        symbol,
        side,
        volume,
        price
    ):

        trade = {
            "symbol": symbol,
            "side": side,
            "volume": volume,
            "entry": price,
            "profit": 0
        }

        self.positions.append(trade)

        return trade



    def close_trade(
        self,
        index,
        exit_price
    ):

        trade = self.positions[index]


        if trade["side"] == "BUY":

            profit = (
                exit_price - trade["entry"]
            ) * trade["volume"]

        else:

            profit = (
                trade["entry"] - exit_price
            ) * trade["volume"]


        trade["profit"] = profit

        self.balance += profit

        return trade