from api_handler import load_data_from_json
from create_msg import create_msg_telegram
import requests


# Define your bot token and chat ID here
BOT_TOKEN = "7025704078:AAF-P5aLqWxc0DFJO81GkOn03S4UU1hHQJ0"
CHAT_ID = "-1002424155477"


def send_api_data_to_telegram(api_data):
    """
    Sends API data to a specified Telegram chat using a bot.

    :param api_data: Data to be sent to Telegram.
    """
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    # Extract the job messages
    job_messages = create_msg_telegram().split(
        '---------------------------------------------------------------------------------------------\n')

    # Remove empty messages that may result from splitting
    job_messages = [msg.strip() for msg in job_messages if msg.strip()]

    # Send each job message separately
    responses = []
    for job_message in job_messages:
        payload = {
            "chat_id": CHAT_ID,
            "text": job_message,
            "parse_mode": "HTML"  # Optional: Formats text as HTML
        }

        # Send the message
        response = requests.post(api_url, json=payload)
        responses.append(response.json())

    return responses


def main():
    # Sample API data to test the function
    sample_data = [
        {
            "title": "Software Engineer",
            "company": "Tech Corp",
            "location": "San Francisco, CA",
            "description": "Develop and maintain software applications."
        },
        {
            "title": "Data Scientist",
            "company": "Data Inc.",
            "location": "New York, NY",
            "description": "Analyze and interpret complex data to help companies make decisions."
        }
    ]

    # Send sample data to Telegram
    # response = send_api_data_to_telegram(sample_data)
    #response = send_api_data_to_telegram(create_msg_telegram())

    #print("Response from Telegram API:", response)
    #send_api_data_to_telegram(load_data_from_json())

if __name__ == "__main__":
    main()
