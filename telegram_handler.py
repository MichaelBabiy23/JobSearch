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

    # Format the API data into a message string
    formatted_message = format_api_data(api_data)

    # Prepare payload
    payload = {
        "chat_id": CHAT_ID,
        "text": formatted_message,
        "parse_mode": "HTML"  # Optional: Formats text as HTML
    }

    # Send the message
    response = requests.post(api_url, json=payload)
    return response.json()

def format_api_data(api_data):
    """
    Formats API data into a string for sending to Telegram.

    :param api_data: Data to be formatted.
    :return: Formatted string of the API data.
    """

    #TODO : change the format of telegram report and emails reports

    formatted_message = "API Data:\n\n"
    for item in api_data:
        formatted_message += f"Job Title: {item.get('title', 'N/A')}\n"
        formatted_message += f"Company: {item.get('company', 'N/A')}\n"
        formatted_message += f"Location: {item.get('location', 'N/A')}\n"
        formatted_message += f"Description: {item.get('description', 'N/A')}\n"
        formatted_message += "-" * 40 + "\n"

    return formatted_message

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
    response = send_api_data_to_telegram(sample_data)
    print("Response from Telegram API:", response)

if __name__ == "__main__":
    main()
