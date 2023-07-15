import traceback
from logging import (
    Handler,
    HTTPHandler,
    CRITICAL,
    ERROR,
    WARNING,
    INFO,
    FATAL,
    DEBUG,
    NOTSET,
    Formatter,
    Filter,
    LogRecord,
)

import six
from urllib.parse import urlparse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

NOTSET_COLOR = "#808080"
DEBUG_COLOR = "#00FFFF"
INFO_COLOR = "#00C400"
WARNING_COLOR = "#FFE240"
ERROR_COLOR = "#FF0000"
CRITICAL_COLOR = "#700000"
FATAL_COLOR = CRITICAL_COLOR

COLORS = {
    NOTSET: NOTSET_COLOR,
    DEBUG: DEBUG_COLOR,
    INFO: INFO_COLOR,
    WARNING: WARNING_COLOR,
    ERROR: ERROR_COLOR,
    FATAL: FATAL_COLOR,
    CRITICAL: CRITICAL_COLOR,
}

DEFAULT_EMOJI = ":heavy_exclamation_mark:"

__all__ = ["SlackLogHandler", "SlackLogHTTPHandler", "SlackLogFilter", "NoStacktraceFormatter", "COLORS"]


class NoStacktraceFormatter(Formatter):
    """
    By default, the stacktrace will be formatted as part of the message.
    Since we want the stacktrace to be in the attachment of the Slack message,
     we need a custom formatter to leave it out of the message
    """

    def formatException(self, ei):
        return None

    def format(self, record: LogRecord):
        # Work-around for https://bugs.python.org/issue29056
        saved_exc_text = record.exc_text
        record.exc_text = None
        try:
            return super(NoStacktraceFormatter, self).format(record)
        finally:
            record.exc_text = saved_exc_text


class SlackLogFilter(Filter):
    """
    Logging filter to decide when logging to Slack is requested, using
    the `extra` kwargs:

        `logger.info("...", extra={'notify_slack': True})`
    """

    def filter(self, record):
        return getattr(record, "notify_slack", False)


class SlackLogHandler(Handler):
    def __init__(
        self,
        slack_token: str,
        channel: str,
        stack_trace: bool = True,
        username: str = "Logging Alerts",
        icon_url: str = None,
        icon_emoji: str = None,
        fail_silent: bool = False,
    ) -> None:
        Handler.__init__(self)
        self.formatter = NoStacktraceFormatter()

        self.stack_trace = stack_trace
        self.fail_silent = fail_silent

        self.client = WebClient(token=slack_token)

        self.username = username
        self.icon_url = icon_url
        self.icon_emoji = (
            icon_emoji if (icon_emoji or icon_url) else DEFAULT_EMOJI
        )
        self.channel = channel

    def build_msg(self, record: LogRecord) -> str:
        """
        Build the Slack message
        Args:
            record (LogRecord): The log record
        Returns:
            str: The Slack message text
        """
        return six.text_type(self.format(record))

    def build_trace(self, record: LogRecord, fallback: str) -> dict:
        """
        Build the Slack attachment for the stacktrace
        Args:
            record (LogRecord): The log record
            fallback (str): The fallback message to use if the stacktrace is not available
        Returns:
            dict: The Slack attachment
        """
        trace = {
            "fallback": fallback,
            "color": COLORS.get(record.levelno, NOTSET_COLOR),
        }

        if record.exc_info:
            text = "\n".join(traceback.format_exception(*record.exc_info))
            trace["text"] = f"```{text}```"
        return trace

    def emit(self, record: LogRecord) -> None:
        """
        Emit a record.
        Args:
            record (LogRecord): The log record
        Returns:
            None
        Raises:
            SlackApiError: If the Slack API returns an error and fail_silent is False
        """
        message = self.build_msg(record)
        if self.stack_trace:
            trace = self.build_trace(record, fallback=message)
            attachments = [trace]
        else:
            attachments = None

        try:
            self.client.chat_postMessage(
                text=message,
                channel=self.channel,
                username=self.username,
                icon_url=self.icon_url,
                icon_emoji=self.icon_emoji,
                attachments=attachments,
            )
        except SlackApiError as e:
            if self.fail_silent:
                pass
            else:
                raise e


class SlackLogHTTPHandler(HTTPHandler):
    def __init__(
        self,
        url,
        username=None,
        icon_url=None,
        icon_emoji=None,
        channel=None,
        mention=None,
    ):
        o = urlparse(url)
        is_secure = o.scheme == "https"
        HTTPHandler.__init__(
            self, o.netloc, o.path, method="POST", secure=is_secure
        )
        self.username = username
        self.icon_url = icon_url
        self.icon_emoji = icon_emoji
        self.channel = channel
        self.mention = mention and mention.lstrip("@")

    def mapLogRecord(self, record):
        text = self.format(record)

        if isinstance(self.formatter, SlackFormatter):
            payload = {
                "attachments": [
                    text,
                ],
            }
            if self.mention:
                payload["text"] = "<@{0}>".format(self.mention)
        else:
            if self.mention:
                text = "<@{0}> {1}".format(self.mention, text)
            payload = {
                "text": text,
            }

        if self.username:
            payload["username"] = self.username
        if self.icon_url:
            payload["icon_url"] = self.icon_url
        if self.icon_emoji:
            payload["icon_emoji"] = self.icon_emoji
        if self.channel:
            payload["channel"] = self.channel

        ret = {
            "payload": json.dumps(payload),
        }
        return ret
