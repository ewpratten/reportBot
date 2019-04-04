# Constants.py
#
# This file contains constants
# and a function to concat an 
# endpoint to the base url

base_url = "https://devrant.com/api"
app_id = 3

def toUrl(endpoint: str) -> str:
    return base_url + endpoint
