import time
import schedule
from datetime import datetime
from ui_handler import create_ui, request_and_notify

TIME_OF_SENDING = "08:00"

def job():
    """Function to run the request_and_notify function."""
    request_and_notify()

def schedule_jobs():
    """Schedules the request_and_notify job."""
    schedule.every().sunday.at(TIME_OF_SENDING).do(job)
    schedule.every().monday.at(TIME_OF_SENDING).do(job)
    schedule.every().tuesday.at(TIME_OF_SENDING).do(job)
    schedule.every().wednesday.at(TIME_OF_SENDING).do(job)
    schedule.every().thursday.at(TIME_OF_SENDING).do(job)

def check_and_send():
    """Check if the message should be sent immediately."""
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    # Check if today's job time has already passed
    if current_time > TIME_OF_SENDING:
        job()

if __name__ == "__main__":
    # Schedule the jobs
    schedule_jobs()

    # Run the UI on the main thread
    # create_ui()  # Ensure this is called in the main thread

    # Check if the job should be sent immediately at the start
    check_and_send()

    # Keep the main thread alive and check for scheduled jobs
    while True:
        schedule.run_pending()
        time.sleep(60)  # Sleep for a minute to reduce CPU usage
