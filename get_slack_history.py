import slackclient
import requests

## need to use groups.history instead of channels.history. mofo
BASE_URL = 'https://slack.com/api/'


def get_slack_history(method, api_key, channel_id, count=100):
    """Gets the channel history for the specified channel.

    :param api_key: API key
    :type api_key: str
    :param channel_id: channel ID
    :type channel_id: str
    :type count: number of messages back to fetch
    :type count: int

    :return TBD:
    :rtype: TBD
    """
    params = {
        'token': api_key,
        'channel': channel_id,
        'count': count
    }
    response = requests.get(
        BASE_URL, params=params
    )
    return response

