import json
import os
from tkinter import messagebox


json_file = "querystring.json"
data_json_file = "data.json"

FILE_PATH = "responses.json"


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
def save_data_to_json(data_string):
    with open(data_json_file, 'w') as f:
        f.write(json.dumps(data_string, indent=4))
    messagebox.showinfo("Success", "data saved to JSON file")


# Function to load collected data from JSON file
def load_data_from_data_json():
    if os.path.exists(json_file):
        with open(data_json_file, 'r') as f:
            return json.load(f)
    return {}  # Return empty dictionary if file does not exist


def load_data():
    """Loads existing data from the JSON file."""
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            return json.load(file)
    return []


def save_jobs(jobs):
    """Saves the jobs to the JSON file."""
    with open(FILE_PATH, 'w') as file:
        file.write(json.dumps(jobs, indent=4))