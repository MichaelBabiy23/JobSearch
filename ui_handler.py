import tkinter as tk
from tkinter import ttk
from api_handler import save_data_to_json, load_data_from_json, load_query_from_json, save_query_to_json, send_request
from email_handler import send_email, add_email_to_file, load_emails_from_file
from telegram_handler import send_api_data_to_telegram


# Function to create the UI
def create_ui():
    # Load previous querystring and Telegram data
    data = load_query_from_json()

    # Create the main window
    root = tk.Tk()
    root.title("API Query Editor")

    # Create and place UI elements with descriptions
    tk.Label(root, text="Query Params").grid(row=0, column=0, padx=10, pady=5)

    # Query
    tk.Label(root, text="Query *").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    query_entry = tk.Entry(root, width=50)
    query_entry.grid(row=1, column=1, padx=10, pady=5)
    query_entry.insert(0, data.get("query", ""))  # Load the existing value
    tk.Label(root, text="Example: Node.js developer in New-York,USA").grid(row=1, column=2, padx=10, pady=5, sticky="w")
    tk.Label(root, text="Free-form jobs search query. Include job title and location.").grid(row=2, column=1, padx=10,
                                                                                             pady=5, sticky="w")

    # Page
    tk.Label(root, text="Page (optional)").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    page_entry = tk.Entry(root, width=50)
    page_entry.grid(row=3, column=1, padx=10, pady=5)
    page_entry.insert(0, data.get("page", "1"))  # Default value is 1
    tk.Label(root, text="Page to return (each page includes up to 10 results).").grid(row=4, column=1, padx=10, pady=5,
                                                                                      sticky="w")
    tk.Label(root, text="Default: 1, Allowed values: 1-100").grid(row=4, column=2, padx=10, pady=5, sticky="w")

    # Number of Pages
    tk.Label(root, text="Number of Pages (optional)").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    num_pages_entry = tk.Entry(root, width=50)
    num_pages_entry.grid(row=5, column=1, padx=10, pady=5)
    num_pages_entry.insert(0, data.get("num_pages", "1"))  # Default value is 1
    tk.Label(root, text="Number of pages to return, starting from page 1").grid(row=6, column=1, padx=10, pady=5,
                                                                               sticky="w")
    tk.Label(root, text="Default: 1, Allowed values: 1-20").grid(row=6, column=2, padx=10, pady=5, sticky="w")

    # Date Posted
    tk.Label(root, text="Date Posted (optional)").grid(row=7, column=0, padx=10, pady=5, sticky="w")
    date_posted_entry = tk.Entry(root, width=50)
    date_posted_entry.grid(row=7, column=1, padx=10, pady=5)
    date_posted_entry.insert(0, data.get("date_posted", "all"))  # Default value is 'all'
    tk.Label(root, text="Find jobs posted within the time you specify.").grid(row=8, column=1, padx=10, pady=5,
                                                                              sticky="w")
    tk.Label(root, text="Allowed values: all, today, 3days, week, month").grid(row=8, column=2, padx=10, pady=5,
                                                                               sticky="w")

    # Remote Jobs Only
    tk.Label(root, text="Remote Jobs Only (optional)").grid(row=9, column=0, padx=10, pady=5, sticky="w")
    remote_jobs_combobox = ttk.Combobox(root, values=["True", "False"], width=8, state="readonly")
    remote_jobs_combobox.grid(row=9, column=1, padx=10, pady=5, sticky="w")
    remote_jobs_combobox.set(data.get("remote_jobs_only", "False"))  # Default value is false
    # remote_jobs_entry = tk.Entry(root, width=50)
    # remote_jobs_entry.grid(row=9, column=1, padx=10, pady=5)
    # remote_jobs_entry.insert(0, data.get("remote_jobs_only", "false"))  # Default value is false
    tk.Label(root, text="Find remote jobs only (work from home).").grid(row=10, column=1, padx=10, pady=5, sticky="w")
    tk.Label(root, text="Default: False").grid(row=10, column=2, padx=10, pady=5, sticky="w")

    # Employment Types
    tk.Label(root, text="Employment Types (optional)").grid(row=11, column=0, padx=10, pady=5, sticky="w")
    employment_types_entry = tk.Entry(root, width=50)
    employment_types_entry.grid(row=11, column=1, padx=10, pady=5)
    employment_types_entry.insert(0, data.get("employment_types", ""))  # Default value is empty
    tk.Label(root, text="FULLTIME, CONTRACTOR, PARTTIME, INTERN").grid(row=12, column=1, padx=10, pady=5, sticky="w")

    # Save button
    def save_querystring():
        data = {
            "query": query_entry.get(),
            "page": page_entry.get(),
            "num_pages": num_pages_entry.get(),
            "date_posted": date_posted_entry.get(),
            "remote_jobs_only": remote_jobs_combobox.get(),
            "employment_types": employment_types_entry.get()
        }
        save_query_to_json(data)

    save_button = tk.Button(root, text="Save Query Parameters", command=save_querystring)
    save_button.grid(row=13, column=0, columnspan=2, padx=10, pady=10)

    # Send request and email button
    def request_and_email():
        send_request()
        api_data = load_data_from_json()
        recipient_emails = load_emails_from_file()
        if recipient_emails:
            send_email(api_data, recipient_emails)
        else:
            print("No email addresses found. Please add at least one email.")

    send_button = tk.Button(root, text="Send API Request and Email to All", command=request_and_email)
    send_button.grid(row=14, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()


# Start the UI
if __name__ == "__main__":
    create_ui()
