import requests
import json
from utils import contains_url

# SMMRY API URL BASE
BASE_URL = 'http://api.smmry.com/'


def request_smmry(api_key, data, summary_length=5, summary_keyword_count=3,
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

    :return: parsed SMMRY API response
    :rtype: dict
    """
    params = {
        'SM_API_KEY': api_key,
        'SM_LENGTH': summary_length,
        'SM_KEYWORD_COUNT': summary_keyword_count,
    }
    if contains_url(data):
        # if the provided data is a URL, pass as URL param
        parsed_url = data[1:-1]
        params['SM_URL'] = parsed_url
    # need to do this to avoid percent encoding url
    params_str = '&'.join(
           '%s=%s' % (param, val) for param, val in params.items()
    )
    if summary_quote_avoid:
        params_str += '&SM_QUOTE_AVOID'
    if summary_with_break:
        params_str += '&SM_WITH_BREAK'
    headers = {'Expect': ''}
    
    ##DEBUG
    print "attempting to summarize:", data
    
    
    payload = {'sm_api_input': data}
    response = requests.post(
        BASE_URL,
        headers=headers,
        params=params_str,
        data=payload
    )
    return response


def parse_response(response):
    """Checks that the request went through and that the SMMRY API
    didn't respond with an error message.

    :param response: SMMRY API response
    :type response: requests.response object

    :return: response decoded from JSON
    :rtype: dict
    """
    if response.status_code != 200:
        raise RuntimeError(
            'Request to SMMRY API failed with code {}'.format(
                response.status_code
            )
        )
    parsed_response = json.loads(response.text)
    if 'sm_api_error' in parsed_response.keys():
        raise RuntimeError(
            'SMMRY API failed to summarize {0} with message {1}'.format(
                response.url,
                parsed_response['sm_api_message']
            )
        )
    return parsed_response


def format_response(parsed_response):
    """Formats response as a string that can be easily written to
    Slack.

    :param parsed_response: parsed response from SMMRY API
    :type parsed_response: dict

    :return: formatted_response
    :rtype: str
    """
    return """
    Summary title: {0}
    Summary: {1}
    Keywords: {2}
    """.format(
        parsed_response['sm_api_title'],
        parsed_response['sm_api_content'],
        str(parsed_response['sm_api_keyword_array'])
    )


def summarize_data(smmry_api_key, data):
    """Uses SMMRY API to summarize provided data.

    :param smmry_api_key: SMMRY API key
    :type smmry_api_key: str
    :param data: data to summarize, eithe text block or link to
    external webpage
    :type data: str

    :return: summarized data, as a formatted string
    :rtype: str
    """

    ##DBUG
    print "first attempting to summarize: ", data

    smmry_response = request_smmry(smmry_api_key, data)
    parsed_response = parse_response(smmry_response)
    formatted_response = format_response(parsed_response)
    return formatted_response

