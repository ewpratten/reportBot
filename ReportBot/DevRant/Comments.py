# Comments.py

import requests
from .Constants import toUrl, app_id
from Auth.Auth import Token

def getComment(login: Token, id: int) -> str:
    """
        Gets comment body and poster from id

        @param login Login Token
        @param id comment id
        @return comment
    """

    # Get data form API
    response = requests.get(toUrl(f"/comments/{id}"), params={"app": app_id, "token_id": login.id, "token_key": login.key, "user_id": login.user}).json()

    # Return comment in readable form
    return response["comment"]["body"]

def postComment(login: Token, text: str, id: int):
    response = requests.post(toUrl(f"/devrant/rants/{id}/comments"), data={"app": app_id, "token_id": login.id, "token_key": login.key, "user_id": login.user, "plat":2, "comment":text})
    # print(response)