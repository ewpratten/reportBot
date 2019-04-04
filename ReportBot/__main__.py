# __main__.py
#
# Main file

# Internal
from Auth.Credentials import load
from Auth.Auth import Authenticate
from DevRant.Notifications import getNotifs
from Regex.Report import report_filter
from DevRant.Comments import getComment, postComment
from DevRant.Rant import getAllUsers, getRant

# External
import json
import time
import requests

# hastebin
def paste(content):
    post = requests.post("https://hastebin.com/documents", data=content.encode('utf-8'))
    return "https://hastebin.com/raw/" + post.json()["key"]

# Load config file
config = json.load(open("/etc/ReportBot/conf.json"))

# Get time step
time_step = config["time_step"]*60

# Convert credstring to Credential
cred = load(config["credstring"])

# Log in
auth_token = Authenticate(cred)

while True:
    # Fetch the notifs
    notifs = getNotifs(auth_token)

    # Skip loop if no notifs are found
    if not notifs:
        time.sleep(time_step)
        continue
    
    # Iterate through each mention
    for notif in notifs:
        # Check if the mention was correctly formatted
        offender = report_filter.match(getComment(auth_token, notif["comment_id"]))
        if not offender:
            continue
        
        # Check is the "offender actually posted the rant or a comment"
        offender = offender[1]
        print(f"Found potential offender: @{offender}")

        # Get all users
        users = getAllUsers(getRant(notif["rant_id"]))

        # Do the check
        if offender not in users:
            continue
        
        print("Verified")

        # Post a comment
        postComment(auth_token, f"@{offender} has been reported\n\nJson dump of post: {paste(str(getRant(notif['rant_id'])))}", notif["rant_id"])
        print("Notified")

    # Sleep for time set in config
    time.sleep(time_step)