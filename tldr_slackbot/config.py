"""Parses config file."""

import ConfigParser
import os


CONFIG = ConfigParser.ConfigParser()
CONFIG.read([os.path.expanduser('~/.tldr_slackbot_conf')])
try:
    BOT_TOKEN = CONFIG.get('Slack', 'bot_token')
    BOT_ID = CONFIG.get('Slack', 'bot_id')
    SMMRY_API_KEY = CONFIG.get('SMMRY', 'api_key')
    TLDR_BOT_CONFIG = {
        'bot_token': BOT_TOKEN,
        'bot_id': BOT_ID,
        'smmry_api_key': SMMRY_API_KEY,
    }
except:
    raise RuntimeError('Issue with config file!')

