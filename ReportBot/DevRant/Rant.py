# Rant.py

import requests
from .Constants import toUrl, app_id
from Auth.Auth import Token

def getRant(id: int) -> dict:
    # get rant fro API
    payload = requests.get(toUrl(f"/devrant/rants/{id}"), params={"app": app_id}).json()
    
    return payload

def getAllUsers(rant: dict) -> list:
    users = []
    
    # add the poster
    users.append(rant["rant"]["user_username"])

    # iterate through comments
    for comment in rant["comments"]:
        users.append(comment["user_username"])

    return users