from datetime import datetime
import sqlite3


class TradeDatabase:

    def __init__(self, db_name="trades_history.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """ایجاد جدول معاملات در صورت عدم وجود"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT,
                    side TEXT,
                    volume REAL,
                    entry_price REAL,
                    exit_price REAL,
                    profit REAL,
                    status TEXT,
                    opened_at TEXT,
                    closed_at TEXT
                )
            """)
            conn.commit()

    def add_trade(self, symbol, side, volume, entry_price):
        """ذخیره معامله جدید"""
        opened_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO trades (symbol, side, volume, entry_price, status, opened_at)
                VALUES (?, ?, ?, ?, 'OPEN', ?)
            """,
                (symbol, side, volume, entry_price, opened_at),
            )
            conn.commit()
            return cursor.lastrowid

    def close_trade(self, trade_id, exit_price, profit):
        """ثبت بسته‌شدن معامله و محاسبه سود/زیان"""
        closed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE trades 
                SET exit_price = ?, profit = ?, status = 'CLOSED', closed_at = ?
                WHERE id = ?
            """,
                (exit_price, profit, closed_at, trade_id),
            )
            conn.commit()

    def get_stats(self):
        """محاسبه آمار عملکرد شامل تعداد معاملات، مجموع سود/زیان و نرخ برد (Win Rate)"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # تعداد کل معاملات بسته شده
            cursor.execute(
                "SELECT COUNT(*) FROM trades WHERE status = 'CLOSED'"
            )
            total_closed = cursor.fetchone()[0]

            if total_closed == 0:
                return {
                    "total_trades": 0,
                    "winning_trades": 0,
                    "losing_trades": 0,
                    "win_rate": 0.0,
                    "total_profit": 0.0,
                }

            # تعداد معاملات موفق
            cursor.execute(
                "SELECT COUNT(*) FROM trades WHERE status = 'CLOSED' AND profit > 0"
            )
            winning_trades = cursor.fetchone()[0]

            # تعداد معاملات ناموفق
            cursor.execute(
                "SELECT COUNT(*) FROM trades WHERE status = 'CLOSED' AND profit <= 0"
            )
            losing_trades = cursor.fetchone()[0]

            # مجموع سود یا زیان نهایی
            cursor.execute(
                "SELECT SUM(profit) FROM trades WHERE status = 'CLOSED'"
            )
            total_profit = cursor.fetchone()[0] or 0.0

            # نرخ برد (Win Rate)
            win_rate = (winning_trades / total_closed) * 100

            return {
                "total_trades": total_closed,
                "winning_trades": winning_trades,
                "losing_trades": losing_trades,
                "win_rate": win_rate,
                "total_profit": total_profit,
            }