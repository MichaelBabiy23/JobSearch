from datetime import datetime, timedelta
from json_file_funcs import load_data, load_data_from_data_json, save_jobs


def remove_duplicates():
    new_api_data = load_data_from_data_json()   # load the downloaded api data
    history_jobs = load_data()                  # load all jobs from responses history

    # Get the list of existing job IDs
    existing_ids = set(job['id'] for job in history_jobs)

    # Filter the jobs and create new entries with only id and title
    new_jobs = [
        {'id': job['id'], 'store_date': datetime.now().date().isoformat()}
        for job in new_api_data['jobs'] if job['id'] not in existing_ids
    ]
    history_jobs.extend(new_jobs)
    save_jobs(history_jobs)

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
    remove_duplicates()


if __name__ == "__main__":
    main()