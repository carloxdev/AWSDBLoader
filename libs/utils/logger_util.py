# Python's Libraries
import logging


class LoggerUtil(object):

    @classmethod
    def create(self, _environment):
        level = logging.INFO

        if _environment == "prod":
            level = logging.ERROR

        logging.basicConfig(
            format='[%(levelname)s] %(message)s',
            level=level
        )

        logger = logging.getLogger(__name__)
        return logger


# LEVELS:
# - CRITICAL	50
# - ERROR	40
# - WARNING	30
# - INFO	20
# - DEBUG	10
# - NOTSET	0
