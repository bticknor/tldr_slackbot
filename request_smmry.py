import requests
import json

# SMMRY API URL BASE
BASE_URL = 'http://api.smmry.com/'
# substrings used for identifying string as a URL
URL_IDENTIFIERS = ['.com', '.org', '.edu', '.co']


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
    params = {
        'SM_API_KEY': api_key,
        'SM_LENGTH': summary_length,
        'SM_KEYWORD_COUNT': summary_keyword_count,
    }
    if any(s in data for s in URL_IDENTIFIERS):
        # if the provided data is a URL, pass as URL param
        params['SM_URL'] = data
    # need to do this to avoid percent encoding url
    params_str = '&'.join(
           '%s=%s' % (param, val) for param, val in params.items()
    )
    if summary_quote_avoid:
        params_str += '&SM_QUOTE_AVOID'
    if summary_with_break:
        params_str += '&SM_WITH_BREAK'
    headers = {'Expect': ''}
    payload = {'sm_api_input': data}
    response = requests.post(
        BASE_URL,
        headers=headers,
        params=params_str,
        data=payload
    )
    return response


def parse_response(response):
    """Parses response from SMMRY API.

    :param response: SMMRY API response
    :type response: requests.response object

    :return: TBD!
    """
    pass

