import time
import schedule
from ui_handler import create_ui, request_and_notify


def job():
    """Function to run the request_and_notify function."""
    request_and_notify()


def schedule_jobs():
    """Schedules the request_and_notify job."""
    schedule.every().sunday.at("08:00").do(job)
    schedule.every().monday.at("08:00").do(job)
    schedule.every().tuesday.at("08:00").do(job)
    schedule.every().wednesday.at("08:00").do(job)
    schedule.every().thursday.at("08:00").do(job)


if __name__ == "__main__":
    # Schedule the jobs
    schedule_jobs()

    # Run the UI on the main thread
    create_ui()  # Ensure this is called in the main thread

    # Keep the main thread alive and check for scheduled jobs
    while True:
        schedule.run_pending()
        time.sleep(30)  # Sleep to prevent high CPU usage
