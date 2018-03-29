from django.db import models
import twitter

from .ignore import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET


def get_tweets(screen_name):
    """
    returns twitter feed with settings as described below, contains all related twitter settings
    """
    api = twitter.Api(consumer_key=CONSUMER_KEY,
                     consumer_secret=CONSUMER_SECRET,
                     access_token_key=ACCESS_TOKEN_KEY,
                     access_token_secret=ACCESS_TOKEN_SECRET)

    return api.GetUserTimeline(screen_name=screen_name, exclude_replies=True, include_rts=False)  # includes entities    