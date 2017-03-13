from slackclient import SlackClient
import time
from config import TLDR_BOT_CONFIG
from request_smmry import (
    request_smmry,
    parse_response
)


# SMMRY API key
SMMRY_API_KEY = TLDR_BOT_CONFIG['smmry_api_key']
# bot id
BOT_ID = TLDR_BOT_CONFIG['bot_id']
# slack API key
BOT_TOKEN = TLDR_BOT_CONFIG['bot_token']
# read from event firehose at 1 second intervals
READ_WEBSOCKET_DELAY = 1


## todo: need to identify which channel bot was summoned from,
## todo: then parse that channel's history for what to summarize


def parse_slack_activity(rtm_output):
    """Parses output from slack RTM event firehose.

    :param rtm_output: firehose event output
    :type rtm_output: list

    :return TBD:
    :rtype: TBD
    """
    directed_at_bot = '<@{}>'.format(BOT_ID)
    if rtm_output and len(rtm_output) > 0:
        for event in rtm_output:
            if 'text' in event and directed_at_bot in event['text']:
                print event
                # parse event
    return None


def run_bot_server():
    """Runs the bot server."""
    # instantiate slack client
    client = SlackClient(BOT_TOKEN)
    connected = client.rtm_connect()
    if not connected:
        raise RuntimeError('Slack API connection failed')
    while True:
        ## do bot stuff
        rtm_output = client.rtm_read()
        parse_slack_activity(rtm_output)
        ## end do bot stuff
        time.sleep(READ_WEBSOCKET_DELAY)


if __name__ == '__main__':
    run_bot_server()

