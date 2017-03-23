"""
Module for core bot logic.
"""

import time
from slackclient import SlackClient
from utils import extract_urls
from smmry import summarize_data
from slack import (
    get_channel_history,
    write_slack_message
)


HELP_MESSAGE = """
What's up! I'm a bot for summarizing external links sent over
Slack. Here's how to use me:

@tldr_bot [#channel|@dm|help]

Call me and I'll automatically summarize the most recent external
link posted to the specified channel/dm, outputting the summary to
where you called me from.  If you don't specify a place to look,
I'll just look in the channel/dm where you called me.
"""

CONFUSED_MESSAGE = """
I'm sorry I didn't understand that...try @tldr_bot help for info
regarding how to use me!
"""


def find_bot_commands(bot_id, rtm_output):
    """Parses output from the RTM firehose, looking for references
    to the bot.

    :param bot_id: id of bot
    :type bot_id: str
    :param rtm_output: raw RTM firehose output
    :type rtm_output: records (list of dicts)

    :return: commands to the bot
    :rtype: list, empty if no bot commands found
    """
    bot_called = '<@{}>'.format(bot_id)
    command_events = []
    if rtm_output and len(rtm_output) > 0:
        for event in rtm_output:
            if 'text' in event and bot_called in event['text']:
                command_events.append(event)
    return command_events


def parse_command(bot_id, command_event):
    """Parses the command, returning either the id of a channel in
    which to look for links to summarize, or a prompt for the
    'help' or 'confused' bot messages.

    :param bot_id: id of bot
    :type bot_id: str
    :param command_event: RTM event including a call to the bot
    :type command_event: dict

    :return parsed_command, channel: parsed command and channel it
    came from
    :rtype: 2-tuple of str, first being either:
      1) channel/dm ID
      2) 'helpme'
      3) 'indecipherable
    Second being channel id that command was sourced from.
    """
    channel = command_event['channel']
    command_text_tokens = command_event['text'].split(' ')
    # if no bot arg, get id of current channel
    if len(command_text_tokens) == 1:
        parsed_command = channel
    else:
        # only care about the first token after the bot invocation
        bot_invocation_pos = command_text_tokens.index(
            '<@{}>'.format(bot_id)
        )
        command_token = command_text_tokens[bot_invocation_pos + 1]
        if command_token == 'help':
            # invocation of the help message
            parsed_command = 'helpme'
        elif command_token[:2] == '<#':
            # reference to a public channel
            parsed_command = command_token.split('|')[0][2:]
        elif command_token[:2] == '<@':
            # reference to a direct message
            parsed_command = command_token[2:][:-1]
        else:
            parsed_command = 'indescipherable'
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
    elif parsed_command == 'indecipherable':
        output = CONFUSED_MESSAGE
    else:
        channel_history = get_channel_history(bot_token, parsed_command)
        url_to_summarize = None
        for message in channel_history:
            # ignore all bot messages
            if 'bot_id' in message.keys():
                continue
            contained_urls = extract_urls(message['text'])
            if contained_urls:
                # only get most recent URL from most recent message
                url_to_summarize = contained_urls[-1]
                break
        if url_to_summarize is None:
            raise RuntimeError('I can\'t find the URL to summarize!')
        try:
            output = summarize_data(smmry_api_key, url_to_summarize)
        except RuntimeError as error:
            output = error.message
    write_slack_message(bot_token, channel, output, 'tdlr_bot')


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
    parsed_command, channel = parse_command(bot_id, command_event)
    act_on_command(parsed_command, channel, bot_token, smmry_api_key)

