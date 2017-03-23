"""
Module for core bot logic.
"""

import time
from slackclient import SlackClient
from utils import extract_urls
from smmry import summarize_data
from slack import (
    get_channel_history,
    get_most_recent_url,
    write_slack_message
)


HELP_MESSAGE = """
What's up! I'm a bot for summarizing external links sent over Slack. Here's
how to use me: @tldr_bot [#channel|@dm|help]. Call me and I'll automatically
summarize the most recent external link posted to the specified channel/dm,
outputting the summary to where you called me from.  If you don't specify a
place to look, I'll just look in the channel/dm where you called me.
""".replace('\n', ' ')


def execute_bot(bot_config, rtm_output):
    """Parses output from the RTM firehose, looking for and acting on
    relevant events, which are defined as either:

      1) Direct messages
      2) Group messages where the bot is called using <@{bot_id}>

    ##TODO below
    Handling of events is done asychronously - as soon as a relevant
    event is identified it is handled by a separate process and the bot
    continues to parse the RTM firehose.

    :param bot_config: config params of bot
    :type bot_config: dict
    :param rtm_output: raw RTM firehose output
    :type rtm_output: records (list of dicts)

    :return: commands to the bot
    :rtype: list, empty if no bot commands found
    """
    bot_id = bot_config['bot_id']
    bot_token = bot_config['bot_token']
    smmry_api_key = bot_config['smmry_api_key']
    bot_called = '<@{}>'.format(bot_id)
    command_events = []
    if rtm_output and len(rtm_output) > 0:
        for event in rtm_output:
            if event['type'] == 'message':
                # if this is a bot message, ignore
                if 'subtype' in event.keys():
                    message_subtype = event['subtype']
                    if message_subtype in [
                        'message_changed', 'bot_message'
                    ]:
                        continue
                # if this is a DM
                if event['channel'][0] == 'D':
                    handle_command(bot_id, event, bot_token, smmry_api_key)
                # if its a group message but the bot is called
                elif bot_called in event['text']:
                    handle_command(bot_id, event, bot_token, smmry_api_key)


def parse_command(bot_token, command_event):
    """Parses the command event, first looking for the 'help' arg, and
    if not finding it in the command text fetching the channel history
    and looking for urls.

    :param bot_token: bot token
    :type bot_token: str
    :param command_event: command event to parse
    :type command_event: str

    :return: url to summarize, channel from which command came
    :rtype: 2-tuple of floats
    """
    channel = command_event['channel']
    command_tokens = command_event['text'].split(' ')
    if 'help' in command_tokens:
        parsed_command = 'helpme'
    else:
        channel_history = get_channel_history(bot_token, channel)
        parsed_command = get_most_recent_url(channel_history)
    return (parsed_command, channel)


def act_on_command(parsed_command, channel, bot_token, smmry_api_key):
    """Handles command and writes output to specified channel.

    :param parsed_command: command to handle
    :type parsed command: str
    :param channel: ID of channel to write output message to
    :type channel: str
    :param bot_token: slack token of bot
    :type bot_token: str
    :param smmry_api_key: SMMRY API key
    :type smmry_api_key: str

    :return : output of bot into channel
    :rtype: str
    """
    if parsed_command == 'helpme':
        output = HELP_MESSAGE
    else:
        try:
            output = summarize_data(smmry_api_key, parsed_command)
        except RuntimeError as error:
            output = error.message
    write_slack_message(bot_token, channel, output, 'tldr_bot')


def handle_command(bot_id, command_event, bot_token, smmry_api_key):
    """Parses command event and takes appropriate action.  This logic
    is grouped together for the sake of running it all asynchronously.

    :param bot_id: id of bot
    :type bot_id: str
    :param command_event: command to handle
    :type command_event: dict
    :param bot_token: API token of bot
    :type bot_token: str
    :param smmry_api_key: SMMRY API key
    :type smmry_api_key: str

    :return: None
    """
    parsed_command, channel = parse_command(bot_token, command_event)
    act_on_command(parsed_command, channel, bot_token, smmry_api_key)

