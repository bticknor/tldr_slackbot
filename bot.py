"""
Module for core bot logic.
"""

from slackclient import SlackClient
from utils import extract_urls
from smmry import summarize_data


class Bot(object):
    """Main bot class."""

    help_message = """
    What's up! I'm a bot for summarizing external links sent over
    Slack. Here's how to use me:

    @tldr_bot [#channel|@dm|help]

    Call me and I'll automatically summarize the most recent external
    link posted to the specified channel/dm, outputting the summary to
    where you called me from.  If you don't specify a place to look,
    I'll just look in the channel/dm where you called me.
    """

    confused_message = """
    I'm sorry I didn't understand that...try @tldr_bot help for info
    regarding how to use me!
    """

    def __init__(self, bot_id, token, smmry_api_key):
        self.bot_id = bot_id
        self.token = token
        self.smmry_api_key = smmry_api_key
        # instantiate connection to Slack RTM API
        self.client = SlackClient(BOT_TOKEN)
        if not self.client.rtm_connect():
            raise RuntimeError('Failed to connect to Slack RTM API!')

    def listen(self):
        """Reads from the Slack RTM firehose."""
        return self.client.rtm_read()

    def find_bot_commands(self, rtm_output):
        """Parses output from the RTM firehose, looking for references
        to the bot.

        :param rtm_output: raw RTM firehose output
        :type rtm_output: records (list of dicts)

        :return: commands to the bot
        :rtype: list, empty if no bot commands found
        """
        bot_called = '<@{}>'.format(self.bot_id)
        command_events = []
        if rtm_output and len(rtm_output) > 0:
            for event in rtm_output:
                if 'text' in event and bot_called in event['text']:
                    command_events.append(event)
        return command_events

    def parse_command(self, command_event):
        """Parses the command, returning either the id of a channel in
        which to look for links to summarize, or a prompt for the
        'help' or 'confused' bot messages.

        :param command_event: RTM event including a call to the bot
        :type command_event: dict

        :return parsed_command: parsed command
        :rtype: str, either a channel/dm ID, 'helpme', or
        'indecipherable'
        """
        command_text_tokens = command_event['text'].split(' ')
        # if no bot arg, get id of current channel
        if len(command_text_tokens) == 1:
            parsed_command = command_event['channel']
        # only care about the first token after the bot invocation
        bot_invocation_pos = command_text_tokens.index(
            '<@{}>'.format(self.bot_id)
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
        return parsed_command
        ## TODO: need channel where posted

    def handle_command(self, channel_id):
        """Takes appropriate action using command_event params based on
        command_type.

        ## TODO: rest of docstring
        """
        if command_type == 'helpme':
            return self.help_message
        elif command_type == 'indecipherable':
            return self.confused_message
        else:
            channel_history = get_slack_history(self.token, channel_id)
        url_to_summarize = None
        for message in channel_history:
            contained_urls = extract_urls(message['text'])
            if contained_urls:
                # only get most recent URL from most recent message
                url_to_summarize = contained_urls[-1]
                break
        url_summary = summarize_data(self.smmry_api_key, url)
        return url_summary

    def write_message(self, channel_id):
        # writes message to slack
        ## TODO: this
        pass





