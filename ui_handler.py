import tkinter as tk
from tkinter import ttk
from api_handler import save_data_to_json, load_data_from_json, load_query_from_json, save_query_to_json, send_request
from email_handler import send_email, add_email_to_file, load_emails_from_file
from telegram_handler import send_api_data_to_telegram


def create_ui(
    initial_query="",
    initial_location="Israel",
    initial_distance=-1.0,
    initial_language="",
    initial_date_posted="",
    initial_allowed_job_providers="",
    initial_index=0,
    initial_remote_only="",
    initial_employment_types="fulltime;parttime;intern;contractor",
):
    """
    Creates the UI for the API query editor.
    """

    # Load previous querystring and Telegram data
    data = load_query_from_json()

    # Create the main window
    root = tk.Tk()
    root.title("API Query Editor")

    # Set a theme
    style = ttk.Style(root)
    style.theme_use("clam")

    # Set global font for all widgets
    root.option_add("*TButton.Font", "Arial 16")
    root.option_add("*TLabel.Font", "Arial 16")
    root.option_add("*TEntry.Font", "Arial 16")
    root.option_add("*TCombobox.Font", "Arial 16")

    # Main Frame
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky="nsew")

    # Query
    ttk.Label(main_frame, text="Query *").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    query_entry = ttk.Entry(main_frame, width=50)
    query_entry.grid(row=1, column=1, padx=10, pady=5)
    query_entry.insert(0, initial_query or data.get("query", ""))
    ttk.Label(main_frame, text="Example: Node.js developer in New-York,USA").grid(row=1, column=2, padx=10, pady=5, sticky="w")

    ttk.Label(main_frame, text="Free-form job search query. Include job title and location.").grid(row=2, column=1, padx=10, pady=5, sticky="w")

    # Location
    ttk.Label(main_frame, text="Location *").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    location_entry = ttk.Entry(main_frame, width=50)
    location_entry.grid(row=3, column=1, padx=10, pady=5)
    location_entry.insert(0, initial_location or data.get("location", ""))

    ttk.Label(main_frame, text="City, country, or any other locations.").grid(row=4, column=1, padx=10, pady=5, sticky="w")

    # Distance
    ttk.Label(main_frame, text="Distance (optional)").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    distance_entry = ttk.Entry(main_frame, width=50)
    distance_entry.grid(row=5, column=1, padx=10, pady=5)
    distance_entry.insert(0, str(initial_distance))

    ttk.Label(main_frame, text="Distance to the location in kilometers. Leave blank for all distances.").grid(row=6, column=1, padx=10, pady=5, sticky="w")

    # Language
    ttk.Label(main_frame, text="Language (optional)").grid(row=7, column=0, padx=10, pady=5, sticky="w")
    language_entry = ttk.Entry(main_frame, width=50)
    language_entry.grid(row=7, column=1, padx=10, pady=5)
    language_entry.insert(0, initial_language)

    ttk.Label(main_frame, text="Language for return fields (location, employmentType, etc.).").grid(row=8, column=1, padx=10, pady=5, sticky="w")

    # Date Posted (Combobox)
    ttk.Label(main_frame, text="Date Posted (optional)").grid(row=9, column=0, padx=10, pady=5, sticky="w")
    date_posted_combobox = ttk.Combobox(main_frame, values=["month", "week", "today", "3days"], width=10, state="readonly")
    date_posted_combobox.grid(row=9, column=1, padx=10, pady=5)
    date_posted_combobox.set(initial_date_posted)

    ttk.Label(main_frame, text="Allowed values: month, week, today, 3days").grid(row=10, column=1, padx=10, pady=5, sticky="w")

    # Remote Only
    ttk.Label(main_frame, text="Remote Jobs Only (optional)").grid(row=11, column=0, padx=10, pady=5, sticky="w")
    remote_jobs_combobox = ttk.Combobox(main_frame, values=["True", "False"], width=10, state="readonly")
    remote_jobs_combobox.grid(row=11, column=1, padx=10, pady=5)
    remote_jobs_combobox.set(initial_remote_only)

    ttk.Label(main_frame, text="Find remote jobs only (work from home).").grid(row=12, column=1, padx=10, pady=5, sticky="w")

    # Allowed Job Providers
    ttk.Label(main_frame, text="Allowed Job Providers (optional)").grid(row=13, column=0, padx=10, pady=5, sticky="w")
    allowed_job_providers_entry = ttk.Entry(main_frame, width=50)
    allowed_job_providers_entry.grid(row=13, column=1, padx=10, pady=5)
    allowed_job_providers_entry.insert(0, initial_allowed_job_providers)

    ttk.Label(main_frame, text="Only receive job postings from specific job providers.").grid(row=14, column=1, padx=10, pady=5, sticky="w")

    # Employment Types
    ttk.Label(main_frame, text="Employment Types (optional)").grid(row=15, column=0, padx=10, pady=5, sticky="w")
    employment_types_entry = ttk.Entry(main_frame, width=50)
    employment_types_entry.grid(row=15, column=1, padx=10, pady=5)
    employment_types_entry.insert(0, initial_employment_types)

    ttk.Label(main_frame, text="FULLTIME, CONTRACTOR, PARTTIME, INTERN").grid(row=16, column=1, padx=10, pady=5, sticky="w")

    # Index
    ttk.Label(main_frame, text="Index (optional)").grid(row=17, column=0, padx=10, pady=5, sticky="w")
    index_entry = ttk.Entry(main_frame, width=50)
    index_entry.grid(row=17, column=1, padx=10, pady=5)
    index_entry.insert(0, str(initial_index))

    ttk.Label(main_frame, text="Index of the search. Maximum 10 jobs per request.").grid(row=18, column=1, padx=10, pady=5, sticky="w")

    # Save button
    def save_querystring():
        data = {
            "query": query_entry.get(),
            "location": location_entry.get(),
            "distance": distance_entry.get(),
            "language": language_entry.get(),
            "date_posted": date_posted_combobox.get(),
            "allowed_job_providers": allowed_job_providers_entry.get(),
            "index": index_entry.get(),
            "remote_only": remote_jobs_combobox.get(),
            "employment_types": employment_types_entry.get()
        }
        save_query_to_json(data)

    save_button = ttk.Button(main_frame, text="Save Query Parameters", command=save_querystring)
    save_button.grid(row=19, column=0, columnspan=2, padx=10, pady=10)

    # Send request and email button
    def request_and_email():
        send_request()
        api_data = load_data_from_json()
        recipient_emails = load_emails_from_file()
        if recipient_emails:
            send_email(api_data, recipient_emails)
        else:
            print("No email addresses found. Please add at least one email.")

    send_button = ttk.Button(main_frame, text="Send API Request and Email to All", command=request_and_email)
    send_button.grid(row=20, column=0, columnspan=2, padx=10, pady=10)

    # Adjust window size based on content
    root.update_idletasks()
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate position to center the window
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)

    # Set window size and position
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    root.mainloop()


# Start the UI
if __name__ == "__main__":
    create_ui()
