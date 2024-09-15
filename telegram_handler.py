import requests


class TelegramBot:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def send_message(self, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"  # Optional, can send messages with markdown/HTML
        }
        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                print("Message sent to Telegram group successfully!")
            else:
                print(f"Failed to send message. Error: {response.text}")
        except Exception as e:
            print(f"Error occurred: {e}")


# Function to send API data to Telegram group
def send_api_data_to_telegram(api_data, bot_token, chat_id):
    bot = TelegramBot(bot_token, chat_id)
    # Convert API data to a formatted string
    message = f"<b>API Data:</b>\n<pre>{api_data}</pre>"
    bot.send_message(message)
