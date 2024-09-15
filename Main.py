import requests

# API endpoint
url = "https://jsearch.p.rapidapi.com/search"

# Query parameters (adjust as necessary)
querystring = {
    "query": "Python Developer",  # Example search query
    "page": "1",
    "num_pages": "1"
}

# Request headers including the RapidAPI key
headers = {
    "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

# Send the request
response = requests.get(url, headers=headers, params=querystring)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Get the response data in JSON format
    print(data)  # Print the data
else:
    print(f"Error: {response.status_code} - {response.text}")
