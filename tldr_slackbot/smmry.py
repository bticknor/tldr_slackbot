import logging
import requests
import json
from tldr_slackbot.utils import contains_url

# SMMRY API URL BASE
BASE_URL = 'http://api.smmry.com/'


def request_smmry(api_key, url, summary_length=5, summary_keyword_count=3):
    """Makes a request to the SMMRY API in order to summarize the
    provided URL.

    :param api_key: SMMRY API key
    :type api_key: str
    :param url: URL to summarize
    :type url: str
    :param summary_length: number of sentences returned
    :type summary_length: int
    :param summary_keyword_count: number of top keywords returned
    :type summary_keyword_count: int

    :return: parsed SMMRY API response
    :rtype: dict
    """
    if not contains_url(url):
        logging.info('Not attempting to summarize {0}, invalid URL'.format(
            url
        ))
        raise RuntimeError('Link provided not a valid URL')
    params = ('?SM_LENGTH={length}&SM_API_KEY={api_key}&SM_KEYWORD_COUNT'
              '={keyword_count}&SM_URL={url}')
    params = params.format(
        length=summary_length,
        api_key=api_key,
        keyword_count=summary_keyword_count,
        url=url
    )
    headers = {'Expect': ''}
    response = requests.post(
        BASE_URL + params,
        headers=headers
    )
    return response


def parse_response(response, requested_url):
    """Checks that the request went through and that the SMMRY API
    didn't respond with an error message.

    :param response: SMMRY API response
    :type response: requests.response object
    :param requested_url: url that was summarized
    :type requested_url: str

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
        logging.info('SMMRY failure with message: {0}'.format(
            parsed_response['sm_api_message']
        ))
        raise RuntimeError(
            'SMMRY failed to summarize {0} with message: {1}'.format(
                requested_url,
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


def summarize_data(smmry_api_key, url):
    """Uses SMMRY API to summarize provided URL.

    :param smmry_api_key: SMMRY API key
    :type smmry_api_key: str
    :param url: url to summarize
    :type url: str

    :return: summarized data, as a formatted string
    :rtype: str
    """
    smmry_response = request_smmry(smmry_api_key, url)
    parsed_response = parse_response(smmry_response, url)
    formatted_response = format_response(parsed_response)
    return formatted_response

