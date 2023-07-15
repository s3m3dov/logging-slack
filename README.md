# logging-slack

[![image](https://img.shields.io/pypi/v/log-to-slack.svg?style=flat-square)](https://pypi.python.org/pypi/log-to-slack)
[![image](https://img.shields.io/pypi/wheel/log-to-slack.svg?style=flat-square)](https://pypi.python.org/pypi/log-to-slack)
[![image](https://img.shields.io/pypi/format/log-to-slack.svg?style=flat-square)](https://pypi.python.org/pypi/log-to-slack)
[![image](https://img.shields.io/pypi/pyversions/log-to-slack.svg?style=flat-square)](https://pypi.python.org/pypi/log-to-slack)
[![image](https://img.shields.io/pypi/status/log-to-slack.svg?style=flat-square)](https://pypi.python.org/pypi/log-to-slack)

Python log handler that posts to a Slack channel. Posts to the Slack API
using [Python Slack SDK](https://github.com/slackapi/python-slack-sdk).

Original repos: 
  - Mathias Ose: [slacker_log_handler](https://github.com/mathiasose/slacker_log_handler)
  - [log-to-slack](https://github.com/pandianmn/log_to_slack)
  - [python-slack-logger](https://github.com/junhwi/python-slack-logger/)

## Installation

``` bash
poetry add git+https://github.com/s3m3dov/logging-slack.git
```

## Arguments

### slack_token (required)

Generate a key at <https://api.slack.com/>

### channel (required)

Set which channel id you want to post to, e.g. `C0XXXXXXXXX` or `#random`.

### username

The username that will post to Slack. Defaults to `Logging Alerts`.

### icon_url

URL to an image to use as the icon for the logger user

### icon_emoji

emoji to use as the icon. Overrides icon_url. If neither icon_url nor
icon_emoji is set, ":heavy_exclamation_mark:" will be used.

### fail_silent

Defaults to `False`. If your API key is invalid or for some other reason
the API call returns an error, this option will silently ignore the API
error. If you enable this setting, **make sure you have another log
handler** that will also handle the same log events, or they may be lost
entirely.

## Example Python logging handler

This is how you use log-to-slack as a regular Python
logging handler. This example will send a error message to a slack
channel.

``` python
import logging
import sys
from datetime import datetime
from log_to_slack import SlackLogHandler, NoStacktraceFormatter

logger = logging.getLogger("Daily Report")
logger.setLevel(logging.DEBUG)

""" Adding slack handler """
slack_handler = SlackerLogHandler(
    "xoxb-XXXXX-XXX",  # slack api token
    "C0XXXXXXXXX", # channel id not channel name
    stack_trace=True,
    fail_silent=True,
)
formatter = NoStacktraceFormatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
slack_handler.setFormatter(formatter)
slack_handler.setLevel(logging.ERROR)
logger.addHandler(slack_handler)

if __name__ == "__main__":
    logger.debug("Debug message to slack!")
    logger.info("Info message to slack!")
    logger.warning("Warning message to slack!")

    try:
        x = 5 / 0
    except:
        logger.exception("Exception message to slack!")
        # # you can also use the below statement to log error with trace info
        # logger.error("Error message to slack!", exc_info=True)
```

## Slack message formatting

This example use a subclass that will send a formatted message to a
Slack channel. [Learn More](https://api.slack.com/reference/surfaces/formatting)

``` python
class CustomLogHandler(SlackLogHandler):
    def build_msg(self, record):
        message = "> New message :\n" + record.getMessage()
        return message
```

## License

Apache 2.0

See also: <https://api.slack.com/terms-of-service>
