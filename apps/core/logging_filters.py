import logging
from logging import LogRecord


class MinLenFilter(logging.Filter):
    def filter(self, record: LogRecord):
        return len(record.getMessage()) > 10


class LengthLimit(logging.Filter):
    def filter(self, record: LogRecord):
        return len(record.getMessage()) > 20
