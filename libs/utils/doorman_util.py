# Python's Libraries
import logging

from enum import Enum

# Third-party Libraries
import jwt as pyjwt

# Own's Libraries
from libs.errors.util_error import UtilError
from libs.constans.language_list import Language


class RequestSource(Enum):
    APIGATEWAY = "APIGATEWAY"
    EVENTBRIDGE = "EVENTBRIDGE"


class DoormanUtil(object):

    def __init__(self, _request, _logger=None):
        self.logger = _logger or logging.getLogger(__name__)
        self.request = _request

        self.logger.info(f"Request: {_request}")

    def get_HeaderParam(self, _param_name, _is_required=False):
        if 'header' not in self.request['params']:
            raise UtilError(
                _message="There is no header in node params",
                _error=None,
                _logger=self.logger,
            )

        if self.request['params']['header'] is None:
            raise UtilError(
                _message="Value of header is missing",
                _error=None,
                _logger=self.logger,
            )

        if _param_name not in self.request["params"]["header"]:
            if _is_required:
                raise UtilError(
                    _message=f"There is no {_param_name} in header node",
                    _error=None,
                    _logger=self.logger,
                )
            else:
                return None

        if self.request["params"]["header"][_param_name] is None:
            if _is_required:
                raise UtilError(
                    _message=f"Value of {_param_name} is missing",
                    _error=None,
                    _logger=self.logger,
                )
            else:
                return None

        try:
            value = self.request["params"]["header"][_param_name]
            return value

        except Exception as e:
            raise UtilError(
                _message=str(e),
                _error=str(e),
                _logger=self.logger
            )

    def get_BodyParam(self, _param_name, _is_required=False):
        if 'body' not in self.request:
            raise UtilError(
                _message="There is no body in request data",
                _error=None,
                _logger=self.logger,
            )

        if self.request['body'] is None:
            raise UtilError(
                _message="The body node is null",
                _error=None,
                _logger=self.logger,
            )

        body = self.request['body']
        param_value = None

        if _param_name not in body:
            if _is_required:
                raise UtilError(
                    _message=f"Value of {_param_name} is missing",
                    _error=None,
                    _logger=self.logger,
                )

            param_value = None

        else:
            param_value = body[_param_name]

        return param_value

    def get_RequestSource(self):
        if 'detail' in self.request:
            return RequestSource.EVENTBRIDGE
        else:
            return RequestSource.APIGATEWAY

    def get_DetailParam(self, _param_name, _is_required=False):
        if 'detail' not in self.request:
            raise UtilError(
                _message="There is no detail in event data",
                _error=None,
                _logger=self.logger,
            )

        if self.request['detail'] is None:
            raise UtilError(
                _message="The detail node is null",
                _error=None,
                _logger=self.logger,
            )

        try:
            detail = self.request['detail']
            param_value = None

            if _param_name not in detail or \
                detail[_param_name] is None or \
                    detail[_param_name] == "":
                if _is_required:
                    raise UtilError(
                        _message=f"Value of {_param_name} is missing",
                        _error=None,
                        _logger=self.logger,
                    )

                param_value = None

            else:
                param_value = detail[_param_name]

            return param_value

        except Exception as e:
            raise UtilError(
                _message=str(e),
                _error=str(e),
                _logger=self.logger
            )

    def get_QueryParam(self, _param_name, _is_required=False):
        if 'params' not in self.request:
            if _is_required:
                raise UtilError(
                    _message="There is no params in request data",
                    _error=None,
                    _logger=self.logger,
                )
            else:
                return None

        if 'querystring' not in self.request['params']:
            if _is_required:
                raise UtilError(
                    _message="There is no querystring in request data",
                    _error=None,
                    _logger=self.logger,
                )
            else:
                return None

        if self.request['params']['querystring'] is None:
            if _is_required:
                raise UtilError(
                    _message="The querystring node is null",
                    _error=None,
                    _logger=self.logger,
                )
            else:
                return None

        if _param_name not in self.request['params']['querystring']:
            if _is_required:
                raise UtilError(
                    _message=f"There is no {_param_name} in queryStringParameters",
                    _error=None,
                    _logger=self.logger,
                )
            else:
                return None

        try:
            query_parameters = self.request['params']['querystring']
            param_value = None

            if query_parameters[_param_name] is None or \
                    query_parameters[_param_name] == "":
                if _is_required:
                    raise UtilError(
                        _message=f"Value of {_param_name} is missing",
                        _error=None,
                        _logger=self.logger,
                    )

                param_value = None

            else:
                param_value = query_parameters[_param_name]

            return param_value

        except Exception as e:
            raise UtilError(
                _message=str(e),
                _error=str(e),
                _logger=self.logger
            )

    def get_PathParam(self, _param_name, _is_required=False):
        if 'params' not in self.request:
            if _is_required:
                raise UtilError(
                    _message="There is no params in request data",
                    _error=None,
                    _logger=self.logger,
                )
            else:
                return None

        if 'path' not in self.request['params']:
            if _is_required:
                raise UtilError(
                    _message="There is no path in node params",
                    _error=None,
                    _logger=self.logger,
                )
            else:
                return None

        if 'path' not in self.request['params']:
            if _is_required:
                raise UtilError(
                    _message="There is no path in node params",
                    _error=None,
                    _logger=self.logger,
                )
            else:
                return None

        if _param_name not in self.request['params']['path']:
            if _is_required:
                raise UtilError(
                    _message=f"There is no {_param_name} in path",
                    _error=None,
                    _logger=self.logger,
                )
            else:
                return None

        try:
            path_parameters = self.request['params']['path']
            param_value = None

            if path_parameters[_param_name] is None or \
                    path_parameters[_param_name] == "":
                if _is_required:
                    raise UtilError(
                        _message=f"Value of {_param_name} is missing",
                        _error=None,
                        _logger=self.logger,
                    )

                param_value = None

            else:
                param_value = path_parameters[_param_name]

            return param_value

        except Exception as e:
            raise UtilError(
                _message=str(e),
                _error=str(e),
                _logger=self.logger
            )

    def response_Success(self, _payload=None, _status_code=200):
        response = {
            'isBase64Encoded': False,
            'statusCode': _status_code,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': "Content-Type,Authorization,x-apigateway-header,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "GET, POST, PATCH, OPTIONS, DELETE"
            },
            'body': _payload
        }

        self.logger.info(response)
        return response

    def response_UserError(self, _message, _code=400):
        raise NameError(f"[BadRequest] {_message}")

    def response_SystemError(self, _message, _code=503):
        raise NameError(f"[InternalServerError] {_message}")

    def response_NotFoundError(self, _message, _code=404):
        raise NameError(f"[NotFound] {_message}")

    def response_Forbidden(self, _message, _code=403):
        self.logger.error(_message)
        raise NameError(f"[Forbidden] {_message}")

    def check_Language(self, _lang):
        if _lang:
            lang = _lang.lower()
            if lang in [e.value for e in Language]:
                return lang
            else:
                raise UtilError(
                    f"Value {_lang} is not a key for a laguage"
                )
        else:
            return Language.ES.value

    def check_Limit(self, _limit):
        try:
            limit = int(_limit) if _limit else 10
            return limit

        except Exception:
            raise UtilError("Limit value should be a number")

    def check_Offset(self, _offset, _default=None):
        try:
            if _offset:
                offset = int(_offset)
                return offset

            else:
                if _default:
                    return _default
                else:
                    return None

        except Exception:
            raise UtilError("Offset value should be a number")

    def get_Username_FromToken(self, _auth):
        PREFIX = 'Bearer '
        token = _auth[len(PREFIX):]
        try:
            jwt_obj = pyjwt.decode(
                token,
                "secret",
                algorithms=["RS256"],
                options={"verify_signature": False}
            )

        except Exception as e:
            self.logger(str(e))
            raise NameError(
                "Something went wrong decoding username from Auth Token"
            )

        if "cognito:username" not in jwt_obj:
            msg = "There is not Username in Auth Token"
            self.logger(msg)
            raise NameError(msg)

        return jwt_obj["cognito:username"]

    def get_PayloadOfListWithLinks(
        self,
        _data,
        _environment=None,
        _endpoint_name=None,
        _offset_id=None,
        _limit=None,
        _lang=None
    ):
        data_response = {}
        data_response['items'] = []
        data_response['links'] = ""

        if _data:
            data_response['items'] = _data

        if _offset_id:
            data_response['links'] = f"{_environment}/{_endpoint_name}?limit={_limit}"
            data_response['links'] = f"{data_response['links']}&offset={_offset_id}"

            if _lang:
                data_response['links'] = f"{data_response['links']}&lang={_lang}"

        return data_response
