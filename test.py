import logging
import os
from platform import python_version

from log_to_slack import SlackLogHandler, NoStacktraceFormatter

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

slack_handler = SlackLogHandler(
    webhook_url=WEBHOOK_URL,
    stack_trace=True,
)
slack_handler.setLevel(logging.WARNING)

logger = logging.getLogger("debug_application")
logger.addHandler(logging.StreamHandler())
logger.addHandler(slack_handler)
logger.setLevel(logging.DEBUG)

formatter = NoStacktraceFormatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
slack_handler.setFormatter(formatter)

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
