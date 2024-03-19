import praw
import os
import re

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import trafilatura


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
        # handle multiples links
        print('link verified')
        summerized_text = summerize_link(verified_link[0])
        commented = bot_commenting(summerized_text, verified_link[0], comment)
        return "summarized commented" if commented else "failed to comment"

    return "no link"

def identify_link(comment):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, comment)
    if 'youtu' in url:
        return False
    return [x[0] for x in url] if len(url) else False

def scrap_website(link):
    ## need to identify the type of website article or offical
    downloaded = trafilatura.fetch_url(link)
    a = trafilatura.extract(downloaded)
    return a

def summerize_link(link):
    #iterate over links
    website_text = scrap_website(link)

    # Parse the input text
    parser = PlaintextParser.from_string(website_text, Tokenizer("english"))

    # Create an LSA summarizer
    summarizer = LsaSummarizer()

    # Generate the summary
    summary = summarizer(parser.document, sentences_count=3)  # You can adjust the number of sentences in the summary

    summary_list = []
    for sentence in summary:
        summary_list.append(' '.join([word for word in sentence.words]))

    return '\n'.join(summary_list)

def bot_commenting(summerized_link_text, link, comment):
    ## posting a new comment with the summerized text
    ## comment.reply()

    message_text = f"""hello, im a summarizer bot. i recognized a link in your comment - {link} and summarized it for you comfort (:
        summary - 
        {summerized_link_text}
    """
    comment_locked = comment.locked
    if not comment_locked:
        response = comment.reply(message_text)

    return comment_locked

if __name__ == "__main__":
    main()