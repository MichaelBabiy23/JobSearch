import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from api_handler import save_data_to_json, load_data_from_data_json, send_request
from create_msg import create_job_msg
from responses_funcs import remove_duplicates
from tkinter import ttk
from json_file_funcs import load_data_from_data_json, load_query_from_json, save_query_to_json
from api_handler import send_request, api_keys
from email_handler import send_email, load_emails_from_file
from telegram_handler import send_api_data_to_telegram

# File to save queries
QUERY_FILE = 'queries.json'


# Load queries from a JSON file
def load_queries():
    if os.path.exists(QUERY_FILE):
        with open(QUERY_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


# Save queries to a JSON file
def save_queries(queries):
    with open(QUERY_FILE, 'w') as f:
        json.dump(queries, f)


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
    # Load previous queries if they exist
    queries = load_queries()

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

    # Query Entry
    ttk.Label(main_frame, text="Query *").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    query_entry = ttk.Entry(main_frame, width=50)
    query_entry.grid(row=1, column=1, padx=10, pady=5)
    query_entry.insert(0, initial_query)

    # Location
    ttk.Label(main_frame, text="Location *").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    location_entry = ttk.Entry(main_frame, width=50)
    location_entry.grid(row=3, column=1, padx=10, pady=5)
    location_entry.insert(0, initial_location)

    # Distance
    ttk.Label(main_frame, text="Distance (optional)").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    distance_entry = ttk.Entry(main_frame, width=50)
    distance_entry.grid(row=5, column=1, padx=10, pady=5)
    distance_entry.insert(0, initial_distance)

    # Language
    ttk.Label(main_frame, text="Language (optional)").grid(row=7, column=0, padx=10, pady=5, sticky="w")
    language_entry = ttk.Entry(main_frame, width=50)
    language_entry.grid(row=7, column=1, padx=10, pady=5)
    language_entry.insert(0, initial_language)

    # Date Posted
    ttk.Label(main_frame, text="Date Posted (optional)").grid(row=9, column=0, padx=10, pady=5, sticky="w")
    date_posted_combobox = ttk.Combobox(main_frame, values=["month", "week", "today", "3days"], width=10,
                                        state="readonly")
    date_posted_combobox.grid(row=9, column=1, padx=10, pady=5)
    date_posted_combobox.set(initial_date_posted)

    # Remote Only
    ttk.Label(main_frame, text="Remote Jobs Only (optional)").grid(row=11, column=0, padx=10, pady=5, sticky="w")
    remote_jobs_combobox = ttk.Combobox(main_frame, values=["True", "False"], width=10, state="readonly")
    remote_jobs_combobox.grid(row=11, column=1, padx=10, pady=5)
    remote_jobs_combobox.set(initial_remote_only)

    # Allowed Job Providers
    ttk.Label(main_frame, text="Allowed Job Providers (optional)").grid(row=13, column=0, padx=10, pady=5, sticky="w")
    allowed_job_providers_entry = ttk.Entry(main_frame, width=50)
    allowed_job_providers_entry.grid(row=13, column=1, padx=10, pady=5)
    allowed_job_providers_entry.insert(0, initial_allowed_job_providers)

    # Employment Types
    ttk.Label(main_frame, text="Employment Types (optional)").grid(row=15, column=0, padx=10, pady=5, sticky="w")
    employment_types_entry = ttk.Entry(main_frame, width=50)
    employment_types_entry.grid(row=15, column=1, padx=10, pady=5)
    employment_types_entry.insert(0, initial_employment_types)

    # Index
    ttk.Label(main_frame, text="Index (optional)").grid(row=17, column=0, padx=10, pady=5, sticky="w")
    index_entry = ttk.Entry(main_frame, width=50)
    index_entry.grid(row=17, column=1, padx=10, pady=5)
    index_entry.insert(0, initial_index)

    # Save button
    def save_querystring():
        query_data = {
            "query": query_entry.get(),
            "location": location_entry.get(),
            "distance": distance_entry.get(),
            "language": language_entry.get(),
            "datePosted": date_posted_combobox.get(),
            "allowedJobProviders": allowed_job_providers_entry.get(),
            "index": index_entry.get(),
            "remoteOnly": remote_jobs_combobox.get(),
            "employmentTypes": employment_types_entry.get()
        }
        queries.append(query_data)
        save_queries(queries)
        populate_query_list()

    save_button = ttk.Button(main_frame, text="Save Query Parameters", command=save_querystring)
    save_button.grid(row=19, column=0, columnspan=2, padx=10, pady=10)

    # Query List
    query_listbox = tk.Listbox(main_frame, selectmode=tk.MULTIPLE, width=80)
    query_listbox.grid(row=20, column=0, columnspan=2, padx=10, pady=10)

    def populate_query_list():
        # print("clearing")
        query_listbox.delete(0, tk.END)  # Clear current list
        for query in queries:
            if isinstance(query, dict) and 'query' in query and 'location' in query and 'isChecked' in query:
                query_listbox.insert(tk.END,
                                     f"{query['query']} - {query['location']} - {"(Will be sent)" if query['isChecked'] else "(Won't be sent)"}")

    # Manage Queries Button
    def show_manage_window():
        manage_window = tk.Toplevel(root)
        manage_window.title("Manage Queries")

        if not queries:
            manage_window.destroy()

        for index, query_data in enumerate(queries):
            frame = ttk.Frame(manage_window)
            frame.pack(fill=tk.X, padx=10, pady=5)

            # Ensure isChecked is in the query_data, default to False if not present
            if 'isChecked' not in query_data:
                query_data['isChecked'] = False

            var = tk.BooleanVar(value=query_data['isChecked'])  # Initialize with current checked state

            # Define a function to update the checkbox state and JSON
            def toggle_check(var, query_data):
                query_data['isChecked'] = var.get()  # Update the JSON entry
                save_queries(queries)  # Save changes to JSON
                populate_query_list()

            checkbox = ttk.Checkbutton(frame, text=query_data.get("query", "Unnamed Query"), variable=var,
                                       command=lambda v=var, q=query_data: toggle_check(v, q))
            checkbox.pack(side=tk.LEFT)

            remove_button = ttk.Button(frame, text="Remove", command=lambda i=index: remove_query(i))
            remove_button.pack(side=tk.RIGHT)

            def remove_query(index):
                del queries[index]
                save_queries(queries)
                manage_window.destroy()
                show_manage_window()  # Refresh the manage window
                populate_query_list()

    # Populate the initial query list
    populate_query_list()

    # Create Manage Queries Button after defining show_manage_window
    manage_button = ttk.Button(main_frame, text="Manage Queries", command=show_manage_window)
    manage_button.grid(row=21, column=0, columnspan=2, padx=10, pady=10)

    # Send Queries Button
    send_button = ttk.Button(main_frame, text="Send Selected Queries", command=request_and_notify)
    send_button.grid(row=22, column=0, columnspan=2, padx=10, pady=10)

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

    # Start the UI
    root.mainloop()


# Send request and notify recipients based on selected queries
def request_and_notify():
    queries = load_queries()
    selected_queries = [query for query in queries if query.get("isChecked")]  # Collect only selected queries
    if not selected_queries:
        messagebox.showwarning("Selection Error", "No queries selected.")
        return

    for query_data in selected_queries:
        send_request(query_data)
        remove_duplicates()

        api_data = load_data_from_data_json()
        for job in api_data['jobs']:
            temp_list = create_job_msg(job)
            job['web'] =  temp_list[0]
            job['description'] =  temp_list[1]
            job['salary'] =  temp_list[2]

        save_data_to_json(api_data)

        recipient_emails = load_emails_from_file()
        if recipient_emails:
            send_email(recipient_emails)
        else:
            print("No email addresses found. Please add at least one email.")

        # Send the data to Telegram
        send_api_data_to_telegram(load_data_from_data_json())


# Start the UI
if __name__ == "__main__":
    # create_ui()
    api_data = load_data_from_data_json()
    recipient_emails = load_emails_from_file()
    if recipient_emails:
        send_email(recipient_emails)
    else:
        print("No email addresses found. Please add at least one email.")

    # Send the data to Telegram
    send_api_data_to_telegram(api_data)