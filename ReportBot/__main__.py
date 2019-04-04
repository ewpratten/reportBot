# __main__.py
#
# Main file

# Internal
from Auth.Credentials import load
from Auth.Auth import Authenticate
from DevRant.Notifications import getNotifs
from Regex.Report import report_filter
from DevRant.Comments import getComment

# External
import json
import time

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
            time.sleep(time_step)
            continue
        
        # Check is the "offender actually posted the rant or a comment"
        offender = offender[1]
        print(f"Found potential offender: @{offender}")

    # Sleep for time set in config
    time.sleep(time_step)