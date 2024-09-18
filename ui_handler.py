import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from api_handler import save_data_to_json, load_data_from_data_json, load_query_from_json, save_query_to_json, \
    send_request
from email_handler import send_email, load_emails_from_file
from telegram_handler import send_api_data_to_telegram

# File to save queries
QUERY_FILE = 'queries.json'


def load_queries():
    """ Load queries from a JSON file. """
    if os.path.exists(QUERY_FILE):
        with open(QUERY_FILE, 'r') as f:
            try:
                return json.load(f)  # Ensure it loads a list of dictionaries
            except json.JSONDecodeError:
                return []  # Return an empty list if the file is empty or invalid
    return []


def save_queries(queries):
    """ Save queries to a JSON file. """
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
    """
    Creates the UI for the API query editor.
    """
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
        query_listbox.delete(0, tk.END)  # Clear current list
        for query in queries:
            if isinstance(query, dict) and 'query' in query and 'location' in query:
                query_listbox.insert(tk.END, f"{query['query']} - {query['location']}")

    # Manage Queries Button
    manage_button = ttk.Button(main_frame, text="Manage Queries", command=lambda: show_manage_window(queries))
    manage_button.grid(row=21, column=0, columnspan=2, padx=10, pady=10)

    # Send Queries Button
    send_button = ttk.Button(main_frame, text="Send Selected Queries", command=request_and_notify)
    send_button.grid(row=22, column=0, columnspan=2, padx=10, pady=10)

    def send_selected_queries():
        selected_indices = query_listbox.curselection()
        if selected_indices:
            selected_queries = [queries[i] for i in selected_indices]
            print("Sending Queries:", selected_queries)  # Replace this with actual sending logic
            messagebox.showinfo("Success", "Selected queries sent successfully!")
        else:
            messagebox.showwarning("Selection Error", "No queries selected.")

    def show_manage_window(queries):
        manage_window = tk.Toplevel(root)
        manage_window.title("Manage Queries")

        for widget in manage_window.winfo_children():
            widget.destroy()

        for index, query_data in enumerate(queries):
            frame = ttk.Frame(manage_window)
            frame.pack(fill=tk.X, padx=10, pady=5)

            var = tk.BooleanVar(value=False)
            checkbox = ttk.Checkbutton(frame, text=query_data.get("query", "Unnamed Query"), variable=var)
            checkbox.pack(side=tk.LEFT)

            remove_button = ttk.Button(frame, text="Remove", command=lambda i=index: remove_query(i))
            remove_button.pack(side=tk.RIGHT)

            # Store variable reference for later use
            queries[index]["send"] = var

        def remove_query(index):
            del queries[index]
            save_queries(queries)
            show_manage_window(queries)  # Refresh the manage window

    # Populate the initial query list
    populate_query_list()

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


# Send request and send data to emails and telegram
def request_and_notify():
    send_request()
    api_data = load_data_from_data_json()
    recipient_emails = load_emails_from_file()
    if recipient_emails:
        send_email(recipient_emails)
    else:
        print("No email addresses found. Please add at least one email.")

    # Send the data to Telegram
    send_api_data_to_telegram(api_data)


# Start the UI
if __name__ == "__main__":
    create_ui()
