from bot import Bot
from config import TLDR_BOT_CONFIG


# SMMRY API key
SMMRY_API_KEY = TLDR_BOT_CONFIG['smmry_api_key']
# bot id
BOT_ID = TLDR_BOT_CONFIG['bot_id']
# slack API key
BOT_TOKEN = TLDR_BOT_CONFIG['bot_token']
# bot username
BOT_USERNAME = TLDR_BOT_CONFIG['bot_username']
# read from event firehose at 1 second intervals
READ_WEBSOCKET_DELAY = 1


if __name__ == '__main__':
    bot = Bot(
        BOT_ID, BOT_TOKEN, SMMRY_API_KEY, BOT_USERNAME,
        READ_WEBSOCKET_DELAY
    )
    bot.run()

