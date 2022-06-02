# Python's Libraries
from datetime import datetime


class TimestampConverter(object):

    @classmethod
    def create_utc_now_timestamp_object(self):
        return datetime.utcnow().isoformat()
