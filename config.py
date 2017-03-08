import ConfigParser
import os


config = ConfigParser.ConfigParser()
config.read([os.path.expanduser('~/.tldr_slackbot_conf')])
try:
    api_key = config.get('tldr_bot Credentials', 'api_key')
    bot_id = config.get('tldr_bot Credentials', 'bot_id')
except ConfigParser.NoSectionError:
    api_key = None
    bot_id = None
finally:
    TLDR_BOT_CONFIG = {
        'api_key': api_key,
        'bot_id': bot_id
    }

