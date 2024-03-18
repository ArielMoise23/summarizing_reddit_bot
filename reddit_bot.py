#!/usr/bin/env python3
from urllib.parse import quote_plus

import praw
import os

QUESTIONS = ["what is", "who is", "what are"]
REPLY_TEMPLATE = "[Let me google that for you](https://lmgtfy.com/?q={})"


def main():
    # All reddit api info
    reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'],
                     client_secret=os.environ['REDDIT_CLIENT_SECRET'],
                     password=os.environ['REDDIT_PASSWORD'],
                     user_agent=os.environ['REDDIT_USER_AGENT'],
                     username=os.environ['REDDIT_USERNAME'])
    

    subreddit = reddit.subreddit("AskReddit")
    for comment in subreddit.stream.comments():
        process_comment(comment)


def process_comment(comment):
    verified_link = identify_link(comment)

    if verified_link:
        summerized_text = summerize_link(verified_link)

    return

def identify_link(comment):
    #link identified or false.
    return 

def summerize_link(link):
    #summerized text of the link.
    return 

def bot_commenting(summerized_link_text):
    ## posting a new comment with the summerized text
    ## comment.reply()
    return

if __name__ == "__main__":
    main()