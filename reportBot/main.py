#!/usr/bin/env python3
import devRantSimple as dRS
import classRant as classes
import os
from pathlib import Path 
import globals as glbl
import requests
import schedule
import time

def post(content):
    post = requests.post("https://hastebin.com/documents", data=content.encode('utf-8'))
    return "https://hastebin.com/raw/" + post.json()["key"]

# Log in
home = str(Path.home())

# Check if config exsists
if os.path.exists(home +'/.reportBot.conf'):
	with open(home + '/.reportBot.conf') as f:
		# load each line into array and remove \n
		content = f.readlines()
		content = [x.strip() for x in content]
		
		# Log in and if successfull, save credentials to global var
		creds = dRS.login(content[0], content[1])
		if creds != dRS.InvalidResponse:
			# Welcome the user
			print("Welcome @" + content[0] + "!")
			glbl.credentials = creds
		else:
			# Force close with code 1
			exit(1)
else:
    print("file not found")
    exit(1)

def loadnotifs():
    uid = glbl.credentials["user_id"]
    token = glbl.credentials["token_id"]
    key = glbl.credentials["token_key"]
    response = dRS.getNotifs(uid, token, key)
    items = response["data"]["items"]
    glbl.mentions = []
    for item in items:
        if item["type"] == "comment_mention":
            # print(item)
            glbl.mentions.append(classes.Notif(item))

def isvalid(mention):
    return True

def sendreport(user, reported, paste, rantid):
    uid = glbl.credentials["user_id"]
    token = glbl.credentials["token_id"]
    key = glbl.credentials["token_key"]

    rant = ""
    rant += "@" + glbl.modname
    rant += "\n\n@"+user+" Has filed a report against "+reported+"\n\n"
    rant += "A raw json snapshot of all comments can be found at:" + paste
    # print(rant)
    dRS.comment(rantid, rant, uid, token, key)

def sendtags(user,rantid):
    uid = glbl.credentials["user_id"]
    token = glbl.credentials["token_id"]
    key = glbl.credentials["token_key"]

    rant = ""
    rant += "@" + glbl.modname
    rant += "\n\n@"+user+" Has reported this rant for improper use of tags"
    # print(rant)
    dRS.comment(rantid, rant, uid, token, key)

def gathersnapshot(rantid):
    rant = classes.Rant(rantid)
    # rant.loadComments()
    # print(rant.comments)
    return post(str(rant.comments))
    # for comment

def loadbanlist():
    # lines = [line.rstrip('\n') for line in open('./banlist.txt', 'r')]
    # glbl.banlist = open('./banlist.txt', 'r')
    with open('banlist.txt','r') as f:
        for line in f:
            for word in line.split():
                glbl.banlist.append(word)

def banadd(username):
    glbl.banlist.append(username)
    banfile = open('./banlist.txt', 'w')
    for item in glbl.banlist:
        print(item)
        banfile.write("%s\n" % item)
    loadbanlist()

def ban(user, banuser, id):
    uid = glbl.credentials["user_id"]
    token = glbl.credentials["token_id"]
    key = glbl.credentials["token_key"]
    banadd(banuser)
    rant = ""
    rant += "\n\n"+banuser+" Is now banned from using reportBot"
    # print(rant)
    dRS.comment(id, rant, uid, token, key)

def respond(mention):
    uid = glbl.credentials["user_id"]
    token = glbl.credentials["token_id"]
    key = glbl.credentials["token_key"]

    
    comment = classes.Comment(dRS.getIdComment(mention.rantId, mention.commentId, uid, token, key)["comment"])
    broken = comment.body.split()

    
    if not mention.isRead:
        print(mention.username)
        if len(broken) >= 2:
            if broken[1] == "tags":
                if mention.username in glbl.trusted:
                    
                    sendtags(mention.username, mention.rantId)
            if broken[1][0] == "@" or broken[1][0] == "b":
                reportname = broken[1]
                if len(broken) >= 3:
                    if broken[1] == "ban":
                        print("ban1")
                        if mention.username in glbl.trusted:
                            print("ban")
                            ban(mention.username, broken[2], mention.rantId)
                    if broken[2] == "report":
                        # if broken[1] != "@dfox" and broken[1] != "@trogus":
                        if mention.username not in glbl.banlist:
                            link = gathersnapshot(mention.rantId)
                            sendreport(mention.username, reportname, link, mention.rantId)

    print(comment.body)
    dRS.clearNotifs(uid, token, key)

def main():
    # idea:
    
    run = True
    loadbanlist()
    print(glbl.banlist)
    while run:
        loadnotifs()
        for mention in glbl.mentions:
            if isvalid(mention):
                respond(mention)
        run = False

main()
# schedule.every(1).minutes.do(main)
# while True:
#     schedule.run_pending()
#     time.sleep(1)