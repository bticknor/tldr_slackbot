"""
Module for core bot logic, defind in the Bot class.

A Bot instance keeps track of (caches) private channels available by
user, since these cannot be referenced by id in slack.  This allows an
invoker of the bot to summarize something posted in a private channel
outside of that private channel, so users must be careful when doing
the bot this way!
"""

from slackclient import SlackClient


class Bot(object):
    """Main bot class."""

    help_message = """
    What's up! I'm a bot for summarizing external links sent over
    Slack. Here's how to use me:

    @tldr_bot [#channel|#private_group|@dm|help]

    Call me and I'll automatically summarize the most recent external
    link posted to the specified channel/private_group/im, outputting
    the summary to where you called me from.  If you don't specify a
    place to look, I'll just look in the channel/group/im where you
    called me.

    BE CAREFUL where you call me when referencing one of your private
    channels, as I will be outputting  a (summarized) post from that
    private channel!
    """

    confused_message = """
    I'm sorry I didn't understand that...try @tldr_bot help for info
    regarding how to use me!
    """

    def __init__(self, bot_id, token):
        self.bot_id = bot_id
        self.token = token
        # instantiate connection to Slack RTM API
        self.client = SlackClient(BOT_TOKEN)
        if not self.client.rtm_connect():
            raise RuntimeError('Failed to connect to Slack RTM API!')
        self.groups = []

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
        """Determines whether the command event to the bot is:

          0) An invocation of the help message
          1) A command to summarize a link sent to a public channel
          2) A command to summarize a link sent to a private channel
          3) A command to summarize a link sent in a direct message
          4) Indecipherable

        The types of 1-3 are referenced by the name of the associated
        Slack API method.

        For 1-3, a channel identifying string is parsed out of the
        command text, for use in the subsequent slack API call.

        These are discrete events because they require different
        actions by the bot.  A 0 requires simple printing of the help
        message, while 1-3 all require calls to different Slack API
        methods. A 4 will result in a simple printing of the "confused"
        message.

        :param command_event: RTM event including a call to the bot
        :type command_event: dict

        :return command_type, channel_id: type of command issued, id of
        channel/group/dm referenced
        :rtype: 2-tuple of strings
        """
        command_text_tokens = command_event['text'].split(' ')
        # only care about the first token after the bot invocation
        bot_invocation_pos = command_text_tokens.index(
            '<@{}>'.format(self.bot_id)
        )
        ## TODO: when nothing specified?!?
        command_token = command_text_tokens[bot_invocation_pos + 1]
        if command_token == 'help':
            # invocation of the help message
            command_type = 'helpme'
            channel_id = ''
        elif command_token[:2] == '<#':
            # reference to a public channel
            command_type = 'channels.history'
            channel_id = command_token.split('|')[0][2:]
        elif command_token[:2] == '<@':
            # reference to a direct message
            command_type = 'im.history'
            channel_id = command_token[2:][:-1]
        elif command_token[0] == '#':
            # reference to a private group
            command_type = 'groups.history'
            channel_id = command_token[1:]
        else:
            command_type = 'indecipherable'
            channel_id = ''
        return command_type, channel_id

    def handle_command(self, command_type, channel_id, command_event):
        """Takes appropriate action using command_event params based on
        command_type.

        ## TODO: rest of docstring
        """
        if command_type == 'helpe':
            return self.help_message
        elif command_type == 'indecipherable':
            return self.confused_message
        else:
            history = get_slack_history(
                command_type, self.token, channel_id
            )
        ## TODO: finish

