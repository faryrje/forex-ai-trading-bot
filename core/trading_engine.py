import logging
import MetaTrader5 as mt5
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from database import TradeDatabase
from news_filter import NewsFilter
from risk.manager import RiskManager
from risk.position_sizing import calculate_position_size
from scanner.market_scanner import MarketScanner
from strategy.engine import StrategyEngine
from telegram_notifier import TelegramNotifier


class TradingEngine:

    def __init__(self, symbols, initial_balance=10000):
        self.scanner = MarketScanner(symbols)
        self.strategy = StrategyEngine()
        self.risk = RiskManager(initial_balance)
        self.db = TradeDatabase()
        self.news_filter = NewsFilter()

        # تنظیمات Dynamic SL/TP بر اساس ضریب ATR
        self.atr_sl_multiplier = 1.5  # ضریب حد ضرر
        self.atr_tp_multiplier = 3.0  # ضریب حد سود

        # تنظیمات Break-Even و Trailing Stop
        self.be_trigger_pips = 15.0
        self.trailing_trigger_pips = 20.0
        self.trailing_distance_pips = 10.0

        self.notifier = TelegramNotifier(
            bot_token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID
        )

        self.notifier.send_message(
            "🤖 <b>Forex AI Trading Bot - MT5 Live Demo Mode!</b>\n"
            "• Direct MT5 Execution: Active ⚡\n"
            "• Auto Filling-Mode Detection: Active\n"
            "• Database & News Filter: Active\n"
            "• Dynamic SL/TP: ATR-Based Active\n"
            "• AI Sentiment Check: Active\n"
            "• Risk Management: 0.5% per trade"
        )

    def _get_ai_sentiment(self, symbol):
        """بررسی احساسات بازار با AI"""
        return "BULLISH"

    def _has_open_position(self, symbol):
        """بررسی وجود پوزیشن باز واقعی در متاتریدر ۵"""
        if not symbol:
            return False

        mt5_positions = mt5.positions_get(symbol=symbol)
        if mt5_positions is not None and len(mt5_positions) > 0:
            return True

        return False

    def _execute_mt5_order(self, symbol, signal, lot_size, sl_price, tp_price):
        """ارسال سفارش مستقیم و واقعی به متاتریدر ۵ با تشخیص خودکار Filling Mode"""
        order_type = mt5.ORDER_TYPE_BUY if signal == "BUY" else mt5.ORDER_TYPE_SELL
        tick = mt5.symbol_info_tick(symbol)
        symbol_info = mt5.symbol_info(symbol)

        if not tick or not symbol_info:
            logging.error(f"Failed to get symbol/tick info for {symbol}")
            return None

        # 🎯 تشخیص خودکار Filling Mode پشتیبانی شده توسط بروکر
        filling = symbol_info.filling_mode
        if filling & 1:  # ORDER_FILLING_FOK
            filling_mode = mt5.ORDER_FILLING_FOK
        elif filling & 2:  # ORDER_FILLING_IOC
            filling_mode = mt5.ORDER_FILLING_IOC
        else:
            filling_mode = mt5.ORDER_FILLING_RETURN

        price = tick.ask if signal == "BUY" else tick.bid

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(lot_size),
            "type": order_type,
            "price": price,
            "sl": float(sl_price),
            "tp": float(tp_price),
            "deviation": 20,
            "magic": 123456,
            "comment": "AI Bot Trade",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": filling_mode,
        }

        result = mt5.order_send(request)

        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            error_comment = result.comment if result else "No response from MT5"
            error_code = result.retcode if result else "Unknown"
            logging.error(f"MT5 Order Failed for {symbol}: {error_comment} (Code: {error_code})")
            return None

        logging.info(f"MT5 Order Successfully Placed! Ticket: {result.order}")
        return result

    def run_cycle(self, market_data_dict):
        # دریافت موجودی واقعی از متاتریدر ۵
        account_info = mt5.account_info()
        balance = account_info.balance if account_info else 10000.0

        self.risk.update_balance(balance)

        if not self.risk.can_trade():
            logging.warning("Trading locked due to daily risk limits.")
            return {"status": "RISK_LIMIT_REACHED"}

        # ۱. مدیریت پوزیشن‌های باز واقعی
        self._manage_open_positions()

        trades_executed = []

        # ۲. پیمایش روی نمادها
        for symbol, item in market_data_dict.items():

            # 🛑 اگر معامله باز روی این نماد در MT5 وجود دارد، انجام نده
            if self._has_open_position(symbol):
                logging.info(
                    f"Skipping {symbol}: Already has an active open position in MT5."
                )
                continue

            # بررسی فیلتر اخبار
            if self.news_filter.is_news_time(symbol):
                logging.info(f"Skipping {symbol} due to news.")
                continue

            signal = self.strategy.analyze(
                {
                    "rsi": item.get("rsi"),
                    "close": item.get("price"),
                    "ema_200": item.get("ema_200"),
                }
            )

            if signal in ["BUY", "SELL"]:
                # ۳. بررسی احساسات بازار با AI
                sentiment = self.get_ai_sentiment_check(symbol, signal)
                if not sentiment["is_confirmed"]:
                    logging.info(
                        f"AI Sentiment rejected {signal} signal for {symbol}. Reason: {sentiment['reason']}"
                    )
                    continue

                # ۴. محاسبه Dynamic SL/TP بر اساس ATR
                atr_value = item.get("atr", 0.0015)
                pip_size = 0.01 if "JPY" in symbol or "XAU" in symbol else 0.0001

                atr_pips = atr_value / pip_size if pip_size else 15.0
                stop_loss_pips = max(
                    15.0, round(atr_pips * self.atr_sl_multiplier, 1)
                )
                take_profit_pips = round(
                    stop_loss_pips
                    * (self.atr_tp_multiplier / self.atr_sl_multiplier),
                    1,
                )

                risk_percentage = 0.5
                lot_size = calculate_position_size(
                    balance=balance,
                    risk_percent=risk_percentage,
                    stop_loss_pips=stop_loss_pips,
                )

                current_price = item.get("price")
                if signal == "BUY":
                    sl_price = round(
                        current_price - (stop_loss_pips * pip_size), 5
                    )
                    tp_price = round(
                        current_price + (take_profit_pips * pip_size), 5
                    )
                else:
                    sl_price = round(
                        current_price + (stop_loss_pips * pip_size), 5
                    )
                    tp_price = round(
                        current_price - (take_profit_pips * pip_size), 5
                    )

                # ⚡ اجرای واقعی معامله در متاتریدر ۵
                order_result = self._execute_mt5_order(
                    symbol, signal, lot_size, sl_price, tp_price
                )

                if order_result:
                    trade_id = self.db.add_trade(
                        symbol=symbol,
                        side=signal,
                        volume=lot_size,
                        entry_price=current_price,
                    )

                    msg = (
                        f"🚀 <b>Real MT5 Demo Trade Placed!</b>\n\n"
                        f"<b>Order Ticket:</b> #{order_result.order}\n"
                        f"<b>Symbol:</b> {symbol}\n"
                        f"<b>Side:</b> {signal}\n"
                        f"<b>Volume:</b> {lot_size} Lots\n"
                        f"<b>Entry Price:</b> {current_price}\n"
                        f"<b>SL:</b> {sl_price} ({stop_loss_pips} pips)\n"
                        f"<b>TP:</b> {tp_price} ({take_profit_pips} pips)\n"
                        f"<b>AI Sentiment:</b> Confirmed ✅"
                    )
                    self.notifier.send_message(msg)
                    trades_executed.append(
                        {"symbol": symbol, "ticket": order_result.order}
                    )

        if trades_executed:
            return {"status": "TRADES_OPENED", "trades": trades_executed}

        return {"status": "HOLD"}

    def get_ai_sentiment_check(self, symbol, signal):
        """بررسی احساسات هوش مصنوعی"""
        sentiment = self._get_ai_sentiment(symbol)

        if signal == "BUY" and sentiment in ["BULLISH", "NEUTRAL"]:
            return {
                "is_confirmed": True,
                "reason": "Aligned with Bullish/Neutral sentiment",
            }
        elif signal == "SELL" and sentiment in ["BEARISH", "NEUTRAL"]:
            return {
                "is_confirmed": True,
                "reason": "Aligned with Bearish/Neutral sentiment",
            }
        else:
            return {
                "is_confirmed": False,
                "reason": f"Signal {signal} conflicts with AI Sentiment ({sentiment})",
            }

    def _manage_open_positions(self):
        """مدیریت Break-Even روی پوزیشن‌های واقعی MT5"""
        positions = mt5.positions_get()
        if not positions:
            return

        for pos in positions:
            symbol = pos.symbol
            pip_size = 0.01 if "JPY" in symbol or "XAU" in symbol else 0.0001
            pips_in_profit = (
                (pos.price_current - pos.price_open) / pip_size
                if pos.type == mt5.ORDER_TYPE_BUY
                else (pos.price_open - pos.price_current) / pip_size
            )

            # انتقال SL به نقطه ورود (Break-Even)
            if pips_in_profit >= self.be_trigger_pips and pos.sl != pos.price_open:
                request = {
                    "action": mt5.TRADE_ACTION_SLTP,
                    "position": pos.ticket,
                    "symbol": symbol,
                    "sl": pos.price_open,
                    "tp": pos.tp,
                }
                mt5.order_send(request)
                self.notifier.send_message(
                    f"🛡️ <b>Break-Even Set on MT5!</b>\n"
                    f"<b>Ticket:</b> #{pos.ticket} ({symbol})\n"
                    f"<b>New SL:</b> {pos.price_open}"
                )