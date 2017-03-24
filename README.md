# Auto-Summarization Bot for Slack

Inspired by the Reddit TLDR Bot, here is a bot that does the same thing on Slack.  The bot works by summarizing external links sent over slack via calls to the SMMRY algorithm API.

## Getting Started

### Installation

Right now, the TLDR bot can only be ```pip```d directly from GitHub, it isn't registered on PyPi:

```pip install git+https://github.com/bticknor/tldr_slackbot```

### Prerequisites

In order to run the TLDR bot, you'll need:
1) A SMMRY API key, which can be obtained here: ```http://smmry.com/api```
2) A Slack bot token, which can be obtained here: ```https://api.slack.com/```
3) The user ID of the bot, available after creation of its token

Getting the user ID of the bot is straightforward, and just involves getting the user list for the relevant Slack team.  Example code showing how to do this via the ```users.list``` API call can be found here:

```https://www.fullstackpython.com/blog/build-first-slack-bot-python.html```

Place a config file named ```.tldr_slackbot_conf``` in your home directory, formatted like so:

```
[Slack]
bot_token={BOT_TOKEN}
bot_id={BOT_ID}

[SMMRY]
api_key={SMMRY_API_KEY}
```

## Running the Bot Server

###TODO: THIS!

## Usage

Usage can be described by the bot itself by calling either ```@tldr_bot help``` in a public channel, or just typing ```help``` into the bot's DM.

In order to summarize an external web page, simply paste the URL of the page into the bot's DM.  To summarize a link posted in a public channel in your slack team, you can either reference that channel in the bot DM by referencing it like so: ```#{CHANNEL_NAME}```, or summarize the link in that channel by calling the bot: ```@tldr_bot```.


