#!/usr/bin/env python
import os
import praw

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def fetch_news(limit=5):
    # create a Reddit instance
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent="YOUR_USER_AGENT_HERE"
    )

    # get the top 5 news from the 'news' subreddit
    subreddit = reddit.subreddit('worldnews')
    top_news = subreddit.top(limit=limit, time_filter='day')
    result = ""
    for i,news in enumerate(top_news):
        result += str(i+1) + ". "+ news.title + "\n"
        result += news.url + "\n\n"

    print(result)
    return result
