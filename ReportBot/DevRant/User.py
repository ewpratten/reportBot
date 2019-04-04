# User.py
#
# Tools to ocnvert to and from a uid

import requests
from .Constants import toUrl, app_id

def fromUID(uid: int) -> str:
    """
        Convert UID to username

        @param uid User ID
        @return username
    """

    # Get data form API
    response = requests.get(toUrl(f"/users/{uid}"), params={"app": app_id}).json()
    
    # Return the username
    return response["profile"]["username"]