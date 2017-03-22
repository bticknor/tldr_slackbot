import json
import slackclient
import requests

BASE_URL = 'https://slack.com/api/'


def request_slack(api_method, params):
    """Sends a request to the Slack API.

    :param api_method: which API method to use
    :type api_method: str
    :param params: url parameters
    :type params: dict mapping str to str

    :return: response
    :rtype: dict
    """
    url = BASE_URL + api_method
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise RuntimeError('Issue connecting to Slack API!')
    decoded_response = json.loads(response.text)
    if not decoded_response['ok']:
        raise RuntimeError('Issue pulling data from Slack API!')
    return decoded_response


def get_channel_history(token, channel_id, count=100):
    """Gets the channel history for the specified channel.

    :param token: API token
    :type token: str
    :param channel_id: channel ID
    :type channel_id: str
    :type count: number of messages back to fetch
    :type count: int

    :return: channel history
    :rtype: records (list of dicts)
    """
    indicator_chars_to_api_methods = {
        'D': 'im.history',
        'C': 'channels.history',
    }
    # first char of id indicates whether it refers to a public channel
    # or DM, which require calls to different API methods to fetch
    # history
    indicator_char = channel_id[0]
    api_method = indicator_chars_to_api_methods[indicator_char]
    params = {
        'token': token,
        'channel': channel_id,
        'count': count
    }
    response = request_slack(api_method, params)
    return response['messages']


def write_slack_message(token, channel_id, message, username):
    """Writes message to slack.

    :param token: API token
    :type token: str
    :param message: message to write
    :type message: str

    :return: None
    """
    api_method = 'chat.postMessage'
    params = {
        'token': token,
        'channel': channel_id,
        'text': message,
        'as_user': False,
        'username': username
    }
    request_slack(api_method, params=params)

