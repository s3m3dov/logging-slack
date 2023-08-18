from logging import Formatter, LogRecord


class DefaultFormatter(Formatter):
    def format(self, record: LogRecord):
        level_name = record.levelname
        seperator = " " * (8 - len(record.levelname))
        record.levelprefix = level_name + ":" + seperator
        return super().format(record)


class NoStacktraceFormatter(DefaultFormatter):
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
