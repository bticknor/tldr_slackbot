from slackclient import SlackClient
import time
from config import TLDR_BOT_CONFIG
from bot import(
    find_bot_commands,
    handle_command
)

# SMMRY API key
SMMRY_API_KEY = TLDR_BOT_CONFIG['smmry_api_key']
# bot id
BOT_ID = TLDR_BOT_CONFIG['bot_id']
# slack API key
BOT_TOKEN = TLDR_BOT_CONFIG['bot_token']
# read from event firehose at 1 second intervals
READ_WEBSOCKET_DELAY = 1


def main():
    """Main function, runs bot server."""
    client = SlackClient(BOT_TOKEN)
    if not client.rtm_connect():
        raise RuntimeError('Failed to connect to Slack RTM API')
    while True:
        rtm_output = client.rtm_read()
        commands = find_bot_commands(BOT_ID, rtm_output)
        for command_event in commands:
            handle_command(
                BOT_ID, command_event, BOT_TOKEN, SMMRY_API_KEY
            )
        time.sleep(READ_WEBSOCKET_DELAY)



if __name__ == '__main__':
    main()

