"""
Module for core bot logic.
"""

import logging
from tldr_slackbot.utils import (
    contains_url
)
from tldr_slackbot.smmry import summarize_data
from tldr_slackbot.slack import (
    get_channel_history,
    get_most_recent_url,
    write_slack_message
)


HELP_MESSAGE = u"""
What's up! I'm a bot for summarizing external links sent over Slack. Here's
how to use me: @tldr_bot [#channel|@dm|help]. Call me and I'll automatically
summarize the most recent external link posted to the specified channel/dm,
outputting the summary to where you called me from.  If you don't specify a
place to look, I'll just look in the channel/dm where you called me.
""".replace('\n', ' ')

CONFUSED_MESSAGE = u"""I'm sorry I don't understand that! Please provide a
link to an external web-page so I can try to summarize it!""".replace(
    '\n', ' '
)


def execute_bot(bot_config, rtm_output):
    """Parses output from the RTM firehose, looking for and acting on
    relevant events, which are defined as either:

      1) Direct messages
      2) Group messages where the bot is called using <@{bot_id}>

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
    if rtm_output and len(rtm_output) > 0:
        for event in rtm_output:
            if is_relevant_event(event, bot_id):
                handle_command(event, bot_token, smmry_api_key)


def is_relevant_event(event, bot_id):
    """Determines whether rtm event is relevant to the bot. Relevant
    events are:

        1) Direct messages to the bot
        2) Messages in public channels where the bot is called

    :param event: event
    :type event: dict
    :param bot_id: id of bot
    :type bot_id: str

    :return: whether the event is relevant, and therefore should be
    acted on by the bot
    :rtype: bool
    """
    bot_called = '<@{}>'.format(bot_id)
    if event['type'] != 'message':
        # ignore all non-messages
        return False
    if 'subtype' in event.keys():
        # ignore bot messages and message changed messages
        if event['subtype'] in ['message_changed', 'bot_message']:
            return False
    if event['channel'][0] == 'D':
        # DM sent to the bot
        return True
    if bot_called in event['text']:
        return True
    return False


def parse_event(bot_token, event):
    """Parses the command event in order to identify the URL to
    summarize, and the channel to write output to. When the 'help'
    arg is provided, the command is indicated as a 'helpme' instead of
    a URL to parse, when the 'help' command is not provided and the
    bot cannot find a URL, it returns 'indecipherable' as the command.

    :param bot_token: bot token
    :type bot_token: str
    :param event: command event to parse
    :type event: str

    :return: url to summarize, channel from which command came
    :rtype: 2-tuple of floats
    """
    channel = event['channel']
    command_tokens = event['text'].split(' ')
    if 'help' in command_tokens:
        # helpme
        parsed_command = 'helpme'
    elif event['channel'][0] == 'D':
        if event['text'][1] == '#':
            # if reference to another channel, get id of that channel
            target_channel = event['text'][2:].split('|')[0]
            # and get history of that channel
            channel_history = get_channel_history(bot_token, target_channel)
            # get URL to page to summarize
            parsed_command = get_most_recent_url(channel_history)
        # if its not a channel reference, assume its a url
        else:
            if not contains_url(event['text']):
                parsed_command = 'indecipherable'
            else:
                parsed_command = event['text'][1:-1]
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
    elif parsed_command == 'indecipherable':
        output = CONFUSED_MESSAGE
    else:
        try:
            logging.info('Attempting to summarize page at %s', parsed_command)
            output = summarize_data(smmry_api_key, parsed_command)
        except RuntimeError as error:
            logging.info(
                'Failed to summarize page at %s with message: %s',
                parsed_command,
                error.message
            )
            output = unicode(error.message)
    write_slack_message(bot_token, channel, output, 'tldr_bot')


def handle_command(command_event, bot_token, smmry_api_key):
    """Parses command event and takes appropriate action.  This logic
    is grouped together for the sake of running it all asynchronously.

    :param command_event: command to handle
    :type command_event: dict
    :param bot_token: API token of bot
    :type bot_token: str
    :param smmry_api_key: SMMRY API key
    :type smmry_api_key: str

    :return: None
    """
    parsed_command, channel = parse_event(bot_token, command_event)
    act_on_command(parsed_command, channel, bot_token, smmry_api_key)

