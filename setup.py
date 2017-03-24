#!/usr/bin/env python

__maintainer__ = "Benjamin Ticknor"
__credits__ = ["Benjamin Ticknor"]
__email__ = "ticknorbenjamin@gmail.com"
__docformat__ = "restructuredtext"

from setuptools import setup, find_packages

# Basics ----------------------------------------------------------------------

NAME = 'tldr_slackbot'
VERSION = '1.0.0'
DESCRIPTION = 'A bot for automatically summarizing links sent over Slack'
LONG_DESCRIPTION = DESCRIPTION

# Dependencies ----------------------------------------------------------------

SETUP_DEPS = ()
INSTALL_DEPS = (
    'configparser==3.5.0',
    'requests==2.13.0',
    'slackclient==1.0.5'
)
EXTRAS_DEPS = {}
TESTS_DEPS = ()
DEPS_SEARCH_URIS = ()

# Entry Point -----------------------------------------------------------------

ENTRY_POINTS = {
    'console_scripts': [
        'run_tldr_bot = tldr_slackbot.run_bot_server:main'
    ]
}

if __name__ == '__main__':
    setup(name=NAME,
          version=VERSION,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          author=', '.join(__credits__),
          maintainer=__maintainer__,
          maintainer_email=__email__,
          setup_requires=SETUP_DEPS,
          install_requires=INSTALL_DEPS,
          extras_require=EXTRAS_DEPS,
          tests_require=TESTS_DEPS,
          packages=find_packages(exclude=['test', 'test.*']),
          include_package_data=True,
          entry_points=ENTRY_POINTS,
          scripts=[])

