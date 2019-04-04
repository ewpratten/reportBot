# Auth.py
#
# Functions for fetching an 
# auth token from devRant

import requests
from DevRant.Constants import toUrl, app_id
from .Credentials import Credential

class Token(object):
    """
        A wrapper class for devRant's auth tokens
    """
    def __init__(self, username, id, token):
        self.user = username
        self.id = id
        self.key = token


def Authenticate(credential: Credential) -> Token:
    """
        Turn a username and password into a Token

        @param username The account username
        @param password The account password
        @return A Token
    """

    # Get payload from server
    try:
        payload = requests.post(toUrl("/users/auth-token"), data={"app": app_id, "username": credential.username, "password": credential.password}).json()
    except:
        print("Something went wrong with login")
        exit(1)
    
    # Return a new Token
    return Token(payload["auth_token"]["user_id"], payload["auth_token"]["id"], payload["auth_token"]["key"])

