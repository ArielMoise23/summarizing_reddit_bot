import praw
import os
import re


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
    verified_link = identify_link(comment.body)

    if verified_link:
        summerized_text = summerize_link(verified_link)

    return

def identify_link(comment):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, comment)
    return [x[0] for x in url] if len(url) else False

def summerize_link(link):
    #iterate over links
    #summerized text of the link.
    return 

def bot_commenting(summerized_link_text):
    ## posting a new comment with the summerized text
    ## comment.reply()
    return

if __name__ == "__main__":
    main()