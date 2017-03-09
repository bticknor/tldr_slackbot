import requests
import json


BASE_URL = 'http://api.smmry.com/&SM_API_KEY={SMMRY_API_KEY}'


def make_request(api_key, data, summary_length=5, summary_keyword_count=3,
        summary_quote_avoid=False, summary_with_break=False):
    """Makes a request to the SMMRY API.

    :param api_key: SMMRY API key
    :type api_key: str
    :param data: one of two things:
        - URL of external webpage to summarize
        - block of text to summarize
    :type data: str
    :param summary_length: number of sentences returned
    :type summary_length: int
    :param summary_keyword_count: number of top keywords returned
    :type summary_keyword_count: int
    :param summary_quote_avoid: whether to avoid quotations
    :type summary_quote_avoid: bool
    :param summary_with_break: whether to include "[BREAK]" between
    sentences
    :type summary_with_break: bool

    :return: SMMRY API response
    :rtype: requests.response object
    """
    params = {}
    headers = {'Expect': ''}
    payload = {'sm_api_input': data}
    response = requests.post(
        BASE_URL.format(SMMRY_API_KEY=api_key),
        data=payload
    )
    ## TODO: figure out URL shit
    return None

