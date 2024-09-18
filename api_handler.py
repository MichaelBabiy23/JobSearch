import requests
import json
import os
from tkinter import messagebox

api_keys = ["aba64a94a8msh1c14f7ec8390ddfp1e091cjsn940fd8e59a12",
            "81d662f1afmshd71bddf20a63757p13654ajsn8b46b22961d6",
            "9d72d9cc25msh53ee03b6851a7f8p1ce3a5jsnfdc0fd11daa4"]

# JSON file to store query information
json_file = "queries.json"
data_json_file = "data.json"
counter_file = "counter.txt"


# Function to save counter to txt file
def save_counter(counter):
    with open(counter_file, 'w') as f:
        f.write(str(counter))


# Function to load counter from txt file
def load_counter():
    if os.path.exists(counter_file):
        with open(counter_file, 'r') as f:
            return int(f.read())
    return 0


counter = load_counter()


# Function to save querystring to JSON file
def save_query_to_json(querystring):
    with open(json_file, 'w') as f:
        json.dump(querystring, f)
    messagebox.showinfo("Success", "Query parameters saved to JSON file")


# Function to load querystring from JSON file
def load_query_from_json():
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            return json.load(f)
    return {}  # Return.exists empty dictionary if file does not exist


# Function to save collected data to JSON file
def save_data_to_json(datastring):
    with open(data_json_file, 'w') as f:
        f.write(json.dumps(datastring, indent=4))
    # messagebox.showinfo("Success", "data saved to JSON file")


# Function to load collected data from JSON file
def load_data_from_data_json():
    if os.path.exists(json_file):
        with open(data_json_file, 'r') as f:
            return json.load(f)
    return {}  # Return empty dictionary if file does not exist


# Function to send the API request using stored querystring
def send_request(querystring):
    global counter

    if not querystring:
        messagebox.showerror("Error", "No query parameters found. Please set the parameters.")
        return

    # Make the API request
    # API endpoint and default headers
    url = "https://jobs-api14.p.rapidapi.com/list"
    headers = {
        "X-RapidAPI-Key": api_keys[counter],
        "X-RapidAPI-Host": "jobs-api14.p.rapidapi.com"
    }

    counter = (counter + 1) % 3
    save_counter(counter)

    response = requests.get(url, headers=headers, params=querystring)

    # Check the status of the request
    if response.status_code == 200:
        data = response.json()
        for job in data['jobs']:
            if job['location'] != "Israel":
                job['location'] = job['location'].replace(", Israel", "").strip()

        # Print the API response in the console
        # print(json.dumps(data, indent=4))
        save_data_to_json(data)
        messagebox.showinfo("Success", "API Request successful. Check console for response.")
    else:
        messagebox.showerror("Error", f"API Request failed: {response.status_code}")


def main():
    send_request()


if __name__ == "__main__":
    main()
