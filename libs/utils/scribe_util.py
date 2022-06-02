# Python's Libraries
from decimal import Decimal
from datetime import datetime
import base64
import json

# Own's Libraries
from libs.errors.util_error import UtilError


class ScribeUtil(object):

    @classmethod
    def encode_Base64(self, _value):
        try:
            value_bytes = _value.encode('ascii')
            bytes_base64 = base64.b64encode(value_bytes)
            value_base64 = bytes_base64.decode('ascii')

            return value_base64

        except Exception as e:
            raise UtilError(
                _message=str(e),
                _error=str(e),
                _logger=None
            )

    @classmethod
    def decode_Base64(self, _value):
        try:
            bytes_base64 = _value.encode('ascii')
            value_bytes = base64.b64decode(bytes_base64)
            value_decode = value_bytes.decode('ascii')

            return value_decode

        except Exception as e:
            raise UtilError(
                _message=str(e),
                _error=str(e),
                _logger=None
            )

    @classmethod
    def get_String_FromDict(self, _dict):
        dict = {}

        for key, value in _dict.items():
            val = value
            if isinstance(value, Decimal):
                val = '{0:2f}'.format(value)

            dict[key] = val

        data_str = json.dumps(dict)
        return data_str

    @classmethod
    def convert_Decimal_ToFloat(self, _decimal_value):
        if _decimal_value is None:
            return None

        else:
            return float(_decimal_value)

    @classmethod
    def encode(self, _value):
        if isinstance(_value, datetime):
            return _value.isoformat()

    @classmethod
    def serialize_Data(self, _data):
        return json.dumps(_data, default=self.encode, ensure_ascii=False)

    @classmethod
    def remove_Trailing_Zeroes(self, _decimal_value):
        if _decimal_value is None:
            return None

        else:
            dec_val = f'{_decimal_value:g}'
            if "." in dec_val:
                return float(_decimal_value)
            else:
                return int(dec_val)
