#--------------Last synchronised with Pylons repo--------------------#
#-----------------------on 5 Feb 2018--------------------------------#
#-------------------------By WU Yan----------------------------------#

import logging, pickle
log = logging.getLogger(__name__)
from S4M_pyramid.model import redis_interface_for_pickle
from twython import Twython,TwythonError
from S4M_pyramid.lib import ttp
from S4M_pyramid.lib.deprecated_pylons_globals import config
from requests import ConnectionError

"""
    Add in number of tweets to show (count)
    also boolean force_refresh  defaults to False
    returns a list
        return[0] is a list of python objects
        return[1] is a dictionary of information about how the info was found
"""

def get_recent_tweets(count,force_refresh=False):
    '''Grabs the given number of most recent tweets tweeted .'''

    label_name = 'twitter_news_cache'

    if not force_refresh:
        result = redis_interface_for_pickle.get(label_name)
        details = {'type':'redis cache'}

        if result is not None:
            return [pickle.loads(result),details]

    try:
        t = Twython(app_key=config['twitter_app_key'],
                    app_secret=config['twitter_app_secret'],
                    oauth_token=config['twitter_oauth_token'],
                    oauth_token_secret=config['twitter_oauth_token_secret'])

        p = ttp.Parser()
        parsed_tweets = []

        screen_name= config['twitter_screen_name']
        tweets = t.get_user_timeline(screen_name=screen_name)[0:count]
        for tweet in tweets:
            parsed_tweets.append(p.parse(tweet))

    except TwythonError:
        log.debug(t._last_call)
        parsed_tweets = []
    except :
        parsed_tweets = []



    result = redis_interface_for_pickle.set(label_name,pickle.dumps(parsed_tweets))
    expiry_time = 600 #seconds, this is 5 minutes
    result = redis_interface_for_pickle.expire(label_name,expiry_time)

    return [parsed_tweets,t._last_call]

