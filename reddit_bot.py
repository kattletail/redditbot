import praw
import config
import time
import os
from player import player

def bot_login():
    print "Logging in..."
    r = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "Babys First Reddit Bot")
    print "Logged in!"
    return r

def run_bot(r, comments_replied_to):
    print "Obtaining 25 most recent comments..."
    
    for comment in r.subreddit('mytestzone').comments(limit=25):
        if "!New_Character" == comment.body and comment.id not in comments_replied_to and not comment.author == r.user.me():
            #Check if user already has a character
            username = str(comment.author)
            if search_player_list(username) == True:
                comment.reply("You already have a character. " +
                              "\n\nAre you sure you want to restart?")
            else:
                newplayer=player(username)
                #comment.reply("You've created a new character, " +
                 #             newplayer.username + "!")
                with open ("player_list.txt", "a") as text_file:
                    text_file.write(newplayer.username + "\n")
                print newplayer.username + " created a new character!"
            print "Replied to comment " + comment.id
            comments_replied_to.append(comment.id)
            with open ("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")

    print "Sleeping for 3 seconds"
    #Sleep for 3 seconds
    time.sleep(3)

def search_player_list(username):
    if not os.path.isfile("player_list.txt"):
        player_list = []
    else:
        with open("player_list.txt", "r") as f:
            player_list = f.read()
            player_list = player_list.split("\n")
            player_list = filter(None, player_list)

    if username in player_list:
        return True
    else:
        return False
        
def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = filter(None, comments_replied_to)
            
    return comments_replied_to

r = bot_login()
comments_replied_to = get_saved_comments()

while True:    
    run_bot(r, comments_replied_to)
