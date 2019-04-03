# Credentials.py
#
# The funcitons contained in this file are used 
# to load, store, and transport login information
#
# -- Credstrings --
# A credstring has the following components:
#
# date = DDMMYYYY Date
# source = base64 encoded name of the program that created the string
# notes = base64 encoded notes / comments about the credstring
# user = base64 encoded username
# pass = base64 encoded password
#
# These are arranged as follows:
# date,source,notes:user,pass
#
# The date, source, and notes are called the DNA


import datetime
from base64 import b64encode, b64decode

class Credential(object):
    """
        A class that represents login information
    """
    def __init__(self, username, password, date, source, notes):
        self.username = username
        self.password = password
        self.date = date
        self.source = source
        self.notes = notes
    
    def toCredstring(self) -> str:
        # Build DNA
        dna = f"{self.date},{b64encode(self.source.encode()).decode()},{b64encode(self.notes.encode()).decode()}"

        # Build user/pass combo
        userpass = f"{b64encode(self.username.encode()).decode()},{b64encode(self.password.encode()).decode()}"

        # Construct credstring
        credstring = f"{dna}:{userpass}"

        # encode credstring
        credstring = b64encode(credstring.encode()).decode()

        return credstring
    
    def __str__(self):
        return f"-- Login --\nUsername: {self.username}\nPassword: {self.password}\n-- DNA --\nDate: {self.date}\nSource: {self.source}\nNotes: {self.notes}"
        


def store(username: str, password: str, notes: str) -> str:
    """
        A function for converting login information into a credstring

        @param username The account username
        @param password The account password
        @param notes Notes about the account (can be blank)

        @return credstring
    """

    # DDMMYYYY Formatted date
    date = datetime.date.today().strftime("%d%m%Y")

    # Name of the program that created the credstring
    source = "ReportBot Credential Manager"

    # Build DNA
    dna = f"{date},{b64encode(source.encode()).decode()},{b64encode(notes.encode()).decode()}"

    # Build user/pass combo
    userpass = f"{b64encode(username.encode()).decode()},{b64encode(password.encode()).decode()}"

    # Construct credstring
    credstring = f"{dna}:{userpass}"

    # encode credstring
    credstring = b64encode(credstring.encode()).decode()
    
    return credstring

def load(credstring: str) -> Credential:
    """
        A function the converts a credstring into a Credential object

        @param credstring The input credstring
        @return A Credential object
    """

    # Decode credstring
    credstring = b64decode(credstring.encode()).decode()

    # Split dna and userpass
    dna, userpass = tuple(credstring.split(":"))

    # Split dna into date, source, and notes
    date, source, notes = tuple(dna.split(","))

    # Decode source and notes
    source = b64decode(source.encode()).decode()
    notes = b64decode(notes.encode()).decode()

    # Split userpass into username and password
    username, password = tuple(userpass.split(","))

    # Decode username and password
    username = b64decode(username.encode()).decode()
    password = b64decode(password.encode()).decode()
    
    # Convert to a Credential and return
    return Credential(username, password, date, source, notes)


# Tests
if __name__ == "__main__":
    # Encode
    creds = store("ewpratten", "test", "test notes")
    print(f"Encoded: {creds}")

    # Decode
    decoded = load(creds)
    print("Decoded:")
    print(decoded)

    print(f"Success: {bool(decoded.toCredstring() == creds)}")
