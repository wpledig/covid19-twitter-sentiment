import tweepy
import sys
import json


def load_twitter_api(api_key_file):
    """
    Connects to the Twitter API via API Keys in a local JSON file
    :param api_key_file: the file location of the API keys (in JSON format)
    :return: a Tweepy API object
    """
    with open(api_key_file) as f:
        keys = json.load(f)
    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True, retry_delay=60 * 3, retry_count=5,
                     retry_errors=set([401, 404, 500, 503]), wait_on_rate_limit_notify=True)

    if not api.verify_credentials():
        print("Your Twitter API credentials are invalid")
        sys.exit()
    else:
        print("Your Twitter API credentials are valid.")

    return api