
class RequestUtil(object):

    def __init__(self):
        self.request_dict = self.__create_BaseRequestDict()

    def __create_BaseRequestDict(self):
        request_dict = {}
        request_dict['params'] = {}
        request_dict['params']['header'] = {}
        request_dict['params']['querystring'] = {}
        request_dict['params']['path'] = {}

        request_dict['body'] = {}
        return request_dict

    def add_BodyParameter(self, _param_name, _param_value):
        self.request_dict['body'][_param_name] = _param_value
        return True

    def add_PathParameter(self, _param_name, _param_value):
        self.request_dict['params']['path'][_param_name] = _param_value
        return True

    def add_QueryParameter(self, _param_name, _param_value):
        self.request_dict['params']['querystring'][_param_name] = _param_value
        return True

    def get_Dict(self):
        return self.request_dict
