"""Utility functions for TLDR bot."""


def contains_url(string):
    """Determines whether string is a URL.

    :param string: string to test
    :type string: str

    :return: whether the string is a URL
    :rtype: bool
    """
    url_identifiers = ['.com', '.org', '.edu', '.co', 'www.', 'http']
    return any(substring in string for substring in url_identifiers)


def extract_urls(string):
    """Returns URL from a sentence - defined here as a space separated
    sequence of words.

    :param string: string from which to extract URL
    :type string: str

    :return: url
    :rtype: str
    """
    split_string = string.split(' ')
    return [word for word in split_string if contains_url(word)]

