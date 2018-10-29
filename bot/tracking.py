import requests

from bot.config import get_env, ENV_PROD

GA_TRACKING_ID = 'UA-128287181-2'
if get_env() == ENV_PROD:
    GA_TRACKING_ID = 'UA-128287181-1'

def track_event(bot_addr, category, action, label=None, value=0):
    data = {
        'v': '1',  # API Version.
        'tid': GA_TRACKING_ID,  # Tracking ID / Property ID.
        # Anonymous Client Identifier. Ideally, this should be a UUID that
        # is associated with particular user, device, or browser instance.
        'cid': bot_addr,
        't': 'event',  # Event hit type.
        'ec': category,  # Event category.
        'ea': action,  # Event action.
        'el': label,  # Event label.
        'ev': value,  # Event value, must be an integer
    }

    requests.post('http://www.google-analytics.com/collect', data=data)
