
import requests
from json_file_funcs import load_data_from_data_json
from create_msg import create_msg_telegram
from responses_funcs import add_jobs_to_responses

# Define your bot token and chat ID here
BOT_TOKEN = "7025704078:AAF-P5aLqWxc0DFJO81GkOn03S4UU1hHQJ0"
CHAT_ID = "-1002424155477"


def send_api_data_to_telegram(api_data):
    """
    Sends API data to a specified Telegram chat using a bot.

    :param api_data: Data to be sent to Telegram.
    """
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    separator = "---------------------------------------------------------------------------------------------\n"

    # Extract the job messages
    job_messages = create_msg_telegram().split(separator)

    # Remove empty messages that may result from splitting
    job_messages = [msg.strip() for msg in job_messages if msg.strip()]

    # Initialize variables to aggregate messages
    current_message = ""
    responses = []

    message_counter = 1

    for job_message in job_messages:
        # Parse the job details from the message
        # print(job_message)
        job_details = parse_job_message(job_message)  # Assuming you create this function
        new_job = {
            "job_name": job_details['job_name'],
            "company": job_details['company'],
            "location": job_details['location'],
            "message": job_message
        }
        # print(new_job)
        # Attempt to add the job, only send if it was added
        if add_jobs_to_responses(new_job):
            # Check if adding the job message exceeds the limit
            if len(current_message) + len(job_message) + 1 > 4096:  # +1 for newline or space
                # Send the current aggregated message
                payload = {
                    "chat_id": CHAT_ID,
                    "text": current_message,
                    "parse_mode": "Markdown"
                }
                # print("sending")
                response = requests.post(api_url, json=payload)
                # checks if message send successfully
                if response.status_code == 200:
                    print(f"Message {message_counter} sent successfully.")
                else:
                    print(f"Message {message_counter} failed.")
                message_counter += 1
                # print(response)
                responses.append(response.json())

                # Start a new message with the current job message
                current_message = job_message
            else:
                # Add the job message to the current message
                if current_message:
                    current_message += "\n" + separator  # Add newline if not the first message
                current_message += job_message

    # Send any remaining messages
    if current_message:
        payload = {
            "chat_id": CHAT_ID,
            "text": current_message,
            "parse_mode": "Markdown"
        }
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            print(f"Message {message_counter} sent successfully.")
        else:
            print(f"Message {message_counter} failed.")
        # print(response)
        responses.append(response.json())

    return responses


def parse_job_message(job_message):
    """Parses job details from the job message string."""
    lines = job_message.split('\n')
    job_name = lines[0].split(': ')[1] if len(lines) > 0 else None
    company_name = lines[1].split(': ')[1] if len(lines) > 1 else None
    location = lines[2].split(': ')[1] if len(lines) > 2 else None
    return {
        "job_name": job_name,
        "company": company_name,
        "location": location
    }

def main():
    # Send sample data to Telegram
    print(send_api_data_to_telegram(load_data_from_data_json()))
    # print(load_data_from_data_json())
    # remove_old_jobs()


if __name__ == "__main__":
    main()
