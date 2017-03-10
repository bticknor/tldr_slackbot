import ConfigParser
import os


config = ConfigParser.ConfigParser()
config.read([os.path.expanduser('~/.tldr_slackbot_conf')])
try:
    slack_api_key = config.get('Slack API Credentials', 'api_key')
    bot_id = config.get('Slack API Credentials', 'bot_id')
    smmry_api_key = config.get('SMMRY API Credentials', 'api_key')
except ConfigParser.NoSectionError:
    slack_api_key = None
    bot_id = None
    smmry_api_key = None
finally:
    TLDR_BOT_CONFIG = {
        'slack_api_key': slack_api_key,
        'bot_id': bot_id,
        'smmry_api_key': smmry_api_key
    }

