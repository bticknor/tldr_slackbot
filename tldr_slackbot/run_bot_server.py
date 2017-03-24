from slackclient import SlackClient
import time
from tldr_slackbot.config import TLDR_BOT_CONFIG
from tldr_slackbot.bot import execute_bot

# read from event firehose at 1 second intervals
READ_WEBSOCKET_DELAY = 1


def main():
    """Main function, runs bot server."""
    client = SlackClient(TLDR_BOT_CONFIG['bot_token'])
    if not client.rtm_connect():
        raise RuntimeError('Failed to connect to Slack RTM API')
    while True:
        rtm_output = client.rtm_read()
        execute_bot(TLDR_BOT_CONFIG, rtm_output)
        time.sleep(READ_WEBSOCKET_DELAY)


if __name__ == '__main__':
    main()

