import requests
import json
import os
from tkinter import messagebox

api_keys = ["aba64a94a8msh1c14f7ec8390ddfp1e091cjsn940fd8e59a12", "81d662f1afmshd71bddf20a63757p13654ajsn8b46b22961d6",
            "9d72d9cc25msh53ee03b6851a7f8p1ce3a5jsnfdc0fd11daa4"]
counter = 0

# JSON file to store query information
json_file = "querystring.json"
data_json_file = "data.json"

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
    return {}  # Return empty dictionary if file does not exist


# Function to save collected data to JSON file
def save_data_to_json(datastring):
    with open(data_json_file, 'w') as f:
        f.write(json.dumps(datastring, indent=4))
    messagebox.showinfo("Success", "data saved to JSON file")

# Function to load collected data from JSON file
def load_data_from_json():
    if os.path.exists(json_file):
        with open(data_json_file, 'r') as f:
            return json.load(f)
    return {}  # Return empty dictionary if file does not exist

# Function to send the API request using stored querystring
def send_request():
    global counter
    # Load querystring from the JSON file
    querystring = load_query_from_json()

    if not querystring:
        messagebox.showerror("Error", "No query parameters found. Please set the parameters.")
        return
    # Make the API request
    # API endpoint and default headers
    url = "jobs-api14.p.rapidapi.com"
    headers = {
        "X-RapidAPI-Key": api_keys[counter],
        "X-RapidAPI-Host": "jobs-api14.p.rapidapi.com"
    }
    counter = (counter + 1) % 3
    response = requests.get(url, headers=headers, params=querystring)

    # Check the status of the request
    if response.status_code == 200:
        data = response.json()
        # Print the API response in the console
        print(data)
        save_data_to_json(data)
        messagebox.showinfo("Success", "API Request successful. Check console for response.")
    else:
        messagebox.showerror("Error", f"API Request failed: {response.status_code}")
