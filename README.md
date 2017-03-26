# Auto-Summarization Bot for Slack

Inspired by the Reddit TLDR Bot, here is a bot that does the same thing on Slack.  The bot works by summarizing external links sent over slack via calls to the SMMRY algorithm API. The bot currently supports:

1) Summarizing webpages of links sent directly to it over DM
2) Summarizing the webpage of the most recent external link sent to a public channel

## Getting Started

### Installation

The TLDR Bot is not registered on PyPi...it can be ```pip```d straight from GitHub: ```pip install git+https://github.com/bticknor/tldr_slackbot```

### Prerequisites

The TLDR Bot handles commands asynchronously with Celery, using Redis as a message broker.  For this reason you'll need Redis installed on the system running the bot server.

For Slack/SMMRY API credentials/info, you'll need:
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

Running the bot involves:
1) Starting a Redis server on localhost port 6379: ```redis-server```
2) Starting a Celery worker using the tldr_slackbot.celery_app app: ```celery worker -A tldr_slackbot.celery_app [OTHER OPTIONS]```
3) Running the bot server: ```run_tldr_bot```

## Usage

Usage can be described by the bot itself by calling either ```@tldr_bot help``` in a public channel, or just typing ```help``` into the bot's DM.

In order to summarize an external web page, simply paste the URL of the page into the bot's DM.  To summarize a link posted in a public channel in your slack team, you can either reference that channel in the bot DM by referencing it like so: ```#{CHANNEL_NAME}```, or summarize the link in that channel by calling the bot: ```@tldr_bot```.


