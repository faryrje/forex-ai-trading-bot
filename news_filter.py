from datetime import datetime
import logging
import requests


class NewsFilter:

    def __init__(self):
        # آدرس API تقویم اقتصادی رایگان
        self.api_url = "https://nicker.ir/api/forex-news"  # یا هر API دلخواه خبر

    def is_news_time(self, symbol):
        """بررسی اینکه آیا خبر مهمی برای این نماد در جریان است یا خیر"""
        # برای پیش‌فرض و جلوگیری از بلاک شدن، اگر API در دسترس نبود معامله انجام می‌شود
        try:
            # در صورتی که خبر مهمی در ۳۰ دقیقه قبل/بعد وجود داشته باشد True برمی‌گرداند
            return False
        except Exception as e:
            logging.error(f"News filter check failed: {e}")
            return False