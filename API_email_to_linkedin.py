import requests

# API base URL
url = "https://api.reversecontact.com/enrichment"

# Query parameters including the API key
querystring = {
    "apikey": "sk_b15fdcd5bf159cd1aa6ca2673a28d61de5454ddf",
    "email": "ritul.koladiya@gmail.com"
}

# Make the GET request
response = requests.get(url, params=querystring)

# Check the response
if response.status_code == 200:
    data = response.json()
    if data.get("success"):
        linkedin_url = data["person"].get("linkedInUrl")
        if linkedin_url:
            print(f"LinkedIn URL: {linkedin_url}")
        else:
            print("LinkedIn URL not found.")
    else:
        print("API call unsuccessful. Check the provided email.")
else:
    print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
    print(f"Response: {response.text}")
