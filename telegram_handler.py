import os
import json
from datetime import datetime, timedelta

import requests
from api_handler import load_data_from_data_json
from create_msg import create_msg_telegram

# Define your bot token and chat ID here
BOT_TOKEN = "7025704078:AAF-P5aLqWxc0DFJO81GkOn03S4UU1hHQJ0"
CHAT_ID = "-1002424155477"
FILE_PATH = "responses.json"


def load_data():
    """Loads existing data from the JSON file."""
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            return json.load(file)
    return []


def save_jobs(jobs):
    """Saves the jobs to the JSON file."""
    with open(FILE_PATH, 'w') as file:
        file.write(json.dumps(jobs, indent=4))


def get_next_id(jobs):
    """Returns the next ID for a new job."""
    if not jobs:
        return 1
    return max(job['id'] for job in jobs) + 1


def add_job(new_job):
    """Adds a new job to the JSON file if it doesn't exist."""
    jobs = load_data()

    # Check if a job with the same name, company, and location already exists
    if not any(
            job['job_name'] == new_job['job_name'] and
            job['company'] == new_job['company'] and
            job['location'] == new_job['location']
            for job in jobs
    ):
        new_job['id'] = get_next_id(jobs)  # Add unique ID
        new_job['store_date'] = datetime.now().date().isoformat()  # Store only the date
        jobs.append(new_job)
        save_jobs(jobs)
        return True
    else:
        return False


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
        if add_job(new_job):
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


def remove_old_jobs():
    """Removes jobs older than one month from the JSON file."""
    jobs = load_data()
    one_month_ago = datetime.now() - timedelta(days=30)

    # Keep only jobs that are not older than one month
    updated_jobs = [
        job for job in jobs
        if datetime.fromisoformat(job['store_date']) > one_month_ago
    ]

    save_jobs(updated_jobs)


def main():
    # Send sample data to Telegram
    print(send_api_data_to_telegram(load_data_from_data_json()))
    # print(load_data_from_data_json())
    # remove_old_jobs()


if __name__ == "__main__":
    main()
