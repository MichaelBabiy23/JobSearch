import tkinter as tk
from api_handler import save_to_json, send_request, load_from_json
from email_handler import send_email, add_email_to_file, load_emails_from_file


# Function to create the UI
def create_ui():
    # Load previous querystring data
    querystring = load_from_json()

    # Create the main window
    root = tk.Tk()
    root.title("API Query Editor")

    # Create and place UI elements
    tk.Label(root, text="Query:").grid(row=0, column=0, padx=10, pady=5)
    query_entry = tk.Entry(root, width=50)
    query_entry.grid(row=0, column=1, padx=10, pady=5)
    query_entry.insert(0, querystring.get("query", ""))  # Load the existing value

    tk.Label(root, text="Page:").grid(row=1, column=0, padx=10, pady=5)
    page_entry = tk.Entry(root, width=50)
    page_entry.grid(row=1, column=1, padx=10, pady=5)
    page_entry.insert(0, querystring.get("page", "1"))  # Default value is 1

    tk.Label(root, text="Number of Pages:").grid(row=2, column=0, padx=10, pady=5)
    num_pages_entry = tk.Entry(root, width=50)
    num_pages_entry.grid(row=2, column=1, padx=10, pady=5)
    num_pages_entry.insert(0, querystring.get("num_pages", "1"))  # Default value is 1

    # Email address section
    tk.Label(root, text="Add Email:").grid(row=3, column=0, padx=10, pady=5)
    email_entry = tk.Entry(root, width=50)
    email_entry.grid(row=3, column=1, padx=10, pady=5)

    # Add email button
    def add_email():
        email = email_entry.get()
        if email:
            add_email_to_file(email)
            email_entry.delete(0, tk.END)  # Clear the entry after adding
        else:
            print("Please enter a valid email address.")

    add_email_button = tk.Button(root, text="Add Email to List", command=add_email)
    add_email_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Save button
    def save_querystring():
        querystring = {
            "query": query_entry.get(),
            "page": page_entry.get(),
            "num_pages": num_pages_entry.get()
        }
        save_to_json(querystring)

    save_button = tk.Button(root, text="Save Query Parameters", command=save_querystring)
    save_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    # Send request and email button
    def request_and_email():
        # Call the API request function and get the response
        send_request()

        # Load the querystring to send as email
        api_data = load_from_json()

        # Load email addresses from emails.txt
        recipient_emails = load_emails_from_file()

        if recipient_emails:
            send_email(api_data, recipient_emails)
        else:
            print("No email addresses found. Please add at least one email.")

    send_button = tk.Button(root, text="Send API Request and Email to All", command=request_and_email)
    send_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    # Start the GUI loop
    root.mainloop()
