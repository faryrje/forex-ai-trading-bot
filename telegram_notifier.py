import logging
import requests


class TelegramNotifier:

    def __init__(self, bot_token=None, chat_id=None):
        self.bot_token = bot_token
        # گرفتن Chat ID و حذف اسپیس‌های اضافی احتمالی
        self.chat_id = str(chat_id).strip() if chat_id else None
        self.enabled = bool(bot_token and chat_id)

    def send_message(self, message: str):
        """ارسال پیام به تلگرام"""
        if not self.enabled:
            return False

        api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML",
        }

        try:
            # تصحیح پارامترها: api_url به عنوان ورودی اول و data=payload
            response = requests.post(api_url, data=payload, timeout=10)
            if response.status_code == 200:
                logging.info("Telegram notification sent successfully.")
                return True
            else:
                logging.error(
                    "Telegram API Error (%s): %s",
                    response.status_code,
                    response.text,
                )
                return False
        except Exception as e:
            logging.error("Failed to send Telegram message: %s", e)
            return False