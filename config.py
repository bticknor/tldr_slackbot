import ConfigParser
import os


config = ConfigParser.ConfigParser()
config.read([os.path.expanduser('~/.tldr_slackbot_conf')])
try:
    bot_token = config.get('Slack API Credentials', 'bot_token')
    bot_id = config.get('Slack API Credentials', 'bot_id')
    smmry_api_key = config.get('SMMRY API Credentials', 'api_key')
    TLDR_BOT_CONFIG = {
        'bot_token': bot_token,
        'bot_id': bot_id,
        'smmry_api_key': smmry_api_key,
    }
except:
    raise RuntimeError('Issue with config file!')

