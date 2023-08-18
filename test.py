import logging
import os
from platform import python_version

from log_to_slack import SlackLogHandler
from log_to_slack.formatters import NoStacktraceFormatter, DefaultFormatter

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

logger = logging.getLogger("debug_application")
logger.setLevel(logging.DEBUG)

default_formatter = DefaultFormatter("%(levelprefix)s %(asctime)s (%(name)s) %(message)s")
no_stacktrace_formatter = NoStacktraceFormatter("%(levelprefix)s %(asctime)s (%(name)s) %(message)s")

default_handler = logging.StreamHandler()
default_handler.setFormatter(default_formatter)
logger.addHandler(default_handler)

slack_handler = SlackLogHandler(webhook_url=WEBHOOK_URL, stack_trace=True)
slack_handler.setFormatter(no_stacktrace_formatter)
slack_handler.setLevel(logging.ERROR)
logger.addHandler(slack_handler)

slack_handler_2 = SlackLogHandler(webhook_url=WEBHOOK_URL, stack_trace=True, traceback_len=8000, msg_len=-1)

# Main code
logger.info("Python version is {}".format(python_version()))

logger.debug("Test DEBUG")
logger.info("Test INFO")
logger.warning("Test WARNING")
logger.error("Test ERROR")
logger.fatal("Test FATAL")
logger.critical("Test CRITICAL")

try:
    raise Exception("Test exception")
except Exception as e:
    logger.exception(e)
