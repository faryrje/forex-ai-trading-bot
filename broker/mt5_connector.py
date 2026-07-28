import logging
import MetaTrader5 as mt5


class MT5Connector:

    def __init__(self):
        self.connected = False

    def connect(self):
        """اتصال به برنامه MetaTrader 5"""
        if not mt5.initialize():
            logging.error(
                "MT5 Initialization failed. Error code: %s", mt5.last_error()
            )
            self.connected = False
            return False

        self.connected = True
        logging.info("Successfully connected to MetaTrader 5")
        return True

    def disconnect(self):
        """قطع اتصال از MT5"""
        mt5.shutdown()
        self.connected = False
        logging.info("Disconnected from MetaTrader 5")

    def get_market_data(self, symbols, timeframe=mt5.TIMEFRAME_M15, count=200):
        """دریافت دیتای زنده کندل‌ها و قیمت برای اسکنر و اندیکاتورها"""
        if not self.connected:
            raise RuntimeError("MT5 is not connected")

        market_data = {}

        for symbol in symbols:
            # اطمینان از فعال بودن نماد در Market Watch
            mt5.symbol_select(symbol, True)

            # دریافت نرخ کندل‌های اخیر
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
            tick = mt5.symbol_info_tick(symbol)

            if rates is not None and len(rates) > 0 and tick is not None:
                prices = [rate["close"] for rate in rates]
                current_price = tick.ask

                market_data[symbol] = prices

                # محاسبه ساده RSI (14) برای داده‌های زنده
                rsi_value = self._calculate_rsi(prices, period=14)
                ema_200 = self._calculate_ema(prices, period=200)

                market_data[f"{symbol}_rsi"] = rsi_value
                market_data[f"{symbol}_ema200"] = ema_200

        return market_data

    def send_order(
        self, symbol, order_type, volume, price=None, stop_loss_pips=30
    ):
        """ارسال سفارش واقعی به متاتریدر ۵"""
        if not self.connected:
            raise RuntimeError("MT5 is not connected")

        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            logging.error("Symbol %s not found", symbol)
            return None

        # تعیین نوع معامله و قیمت ورود
        if order_type == "BUY":
            trade_type = mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(symbol).ask if not price else price
            sl = price - (stop_loss_pips * symbol_info.point * 10)
        elif order_type == "SELL":
            trade_type = mt5.ORDER_TYPE_SELL
            price = mt5.symbol_info_tick(symbol).bid if not price else price
            sl = price + (stop_loss_pips * symbol_info.point * 10)
        else:
            return None

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(volume),
            "type": trade_type,
            "price": price,
            "sl": sl,
            "deviation": 20,
            "magic": 100200,
            "comment": "Forex AI Bot Trade",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error("Order failed! Retcode: %s", result.retcode)
            return {"status": "FAILED", "code": result.retcode}

        logging.info(
            "Order executed successfully! Ticket: %s", result.order
        )
        return {
            "status": "SUCCESS",
            "order_id": result.order,
            "symbol": symbol,
            "volume": volume,
            "price": result.price,
        }

    # --- متدهای کمکی محاسبه اندیکاتورها ---
    def _calculate_rsi(self, prices, period=14):
        if len(prices) < period + 1:
            return None
        gains, losses = [], []
        for i in range(1, len(prices)):
            change = prices[i] - prices[i - 1]
            gains.append(max(change, 0))
            losses.append(max(-change, 0))

        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period

        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        return round(100 - (100 / (1 + rs)), 2)

    def _calculate_ema(self, prices, period=200):
        if len(prices) < period:
            return prices[-1]
        multiplier = 2 / (period + 1)
        ema = prices[0]
        for price in prices[1:]:
            ema = (price - ema) * multiplier + ema
        return round(ema, 5)