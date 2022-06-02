# Python's Libraries
import logging


class BaseError(Exception):

    def __init__(self, _message, _error=None, _logger=None, _source=None,):
        self.logger = _logger or logging.getLogger(__name__)

        self.message = _message
        self.source = _source
        self.error = _error

        self.logger.error(self.__get_FullErrorMsg())

        super().__init__(_message)

    def __get_FullErrorMsg(self):
        value = f'{self.message}'
        if self.source:
            value = f'{value} ({self.source})'

        if self.error:
            value = f'{value}: {self.error}'

        return value

    def __str__(self):
        return self.__get_FullErrorMsg()


class OffsetOutRange(BaseError):
    pass
