# Notifications.py
#
# Load and clear notifications


import requests
from .Constants import toUrl, app_id
from .User import fromUID
from Auth.Auth import Token

def getNotifs(login: Token) -> dict:
    """
        Get unred notifs from devRant API

        @param login Login Token
        @return dict of notifs
    """

    # Get data from server
    response = requests.get(toUrl("/users/me/notif-feed"), params={"app": app_id, "token_id": login.id, "token_key": login.key, "user_id": login.user}).json()
    
    # Create empty list for output
    output = []

    # Add all unread mentions to output
    for item in response["data"]["items"]:
        if item["read"] != 1 and item["type"] == "comment_mention":
            # Output:
            # rant_id: rant_id
            # comment_id: comment_id
            # user: username from uid
            output.append({
                "rant_id": item["rant_id"],
                "comment_id": item["comment_id"],
                "user":fromUID(item["uid"])
            })

    return output