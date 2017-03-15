import json
import slackclient
import requests

## need to use groups.history instead of channels.history. mofo
BASE_URL = 'https://slack.com/api/'


def get_slack_history(token, channel_id, count=100):
    """Gets the channel history for the specified channel.

    :param token: API token
    :type token: str
    :param channel_id: channel ID
    :type channel_id: str
    :type count: number of messages back to fetch
    :type count: int

    :return TBD:
    :rtype: TBD
    """
    indicator_chars_to_api_methods = {
        'U': 'im.history',
        'C': 'channels.history',
    }
    # first char of id indicates whether it refers to a public channel
    # or DM, which require calls to different API methods to fetch
    # history
    indicator_char = channel_id[0]
    api_method = indicator_chars_to_api_methods[indicator_char]
    url = BASE_URL + api_method
    params = {
        'token': token,
        'channel': channel_id,
        'count': count
    }
    response = requests.get(
        url, params=params
    )
    assert response.status_code == 200, 'Issue connecting to Slack API!'
    decoded_response = json.loads(response.text)
    assert decoded_response['ok'], 'Issue pulling data from Slack API!'
    # now parse through responses
    return decoded_response['messages']

