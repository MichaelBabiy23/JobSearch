import requests
import json
import os
from tkinter import messagebox

# API endpoint and default headers
url = "https://jsearch.p.rapidapi.com/search"
headers = {
    "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",  # Replace with your RapidAPI key
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

# JSON file to store query information
json_file = "querystring.json"


# Function to save querystring to JSON file
def save_to_json(querystring):
    with open(json_file, 'w') as f:
        json.dump(querystring, f)
    messagebox.showinfo("Success", "Query parameters saved to JSON file")


# Function to load querystring from JSON file
def load_from_json():
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            return json.load(f)
    return {}  # Return empty dictionary if file does not exist


# Function to send the API request using stored querystring
def send_request():
    # Load querystring from the JSON file
    querystring = load_from_json()

    if not querystring:
        messagebox.showerror("Error", "No query parameters found. Please set the parameters.")
        return

    # Make the API request
    response = requests.get(url, headers=headers, params=querystring)

    # Check the status of the request
    if response.status_code == 200:
        data = response.json()
        # Print the API response in the console
        print(data)
        messagebox.showinfo("Success", "API Request successful. Check console for response.")
    else:
        messagebox.showerror("Error", f"API Request failed: {response.status_code}")
