
from libs.utils.decorators import step
from libs.utils.scribe_util import ScribeUtil


class Payloader(object):

    def __init__(self, _data, _nextpage, _limit):
        self.data = _data
        self.nextpage = _nextpage
        self.limit = _limit

    @step("[Payloader] Getting Parameter Value ...")
    def __get_Parameter(self, _key, _value, _position):
        if _position == 1:
            param = f"?{_key}={_value}"

        else:
            param = f"&{_key}={_value}"

        return param

    @step("[Payloader] Getting Link Node ...")
    def get_LinksNode(self, _extra_params):
        if self.nextpage is None:
            return ""

        links_node = "/exporter-importer"
        count = 1

        if self.nextpage:
            links_node += self.__get_Parameter("offset", self.nextpage, count)
            count += 1

        if self.limit:
            links_node += self.__get_Parameter("limit", self.limit, count)
            count += 1

        if _extra_params:
            for key, value in _extra_params.items():
                if value:
                    links_node += self.__get_Parameter(key, value, count)
                    count += 1

        return links_node

    @step("[Payloader] Getting Data Node ...")
    def get_DataNode(self):
        return ScribeUtil.serialize_Data(self.data)

    @step("[Payloader] Getting Dict ...")
    def get_Dict(self, _extra_params):
        payload = {}

        if len(self.data) == 0:
            payload['items'] = []
            payload['links'] = ""

            return payload

        payload['items'] = self.get_DataNode()
        payload['links'] = self.get_LinksNode(_extra_params)

        return payload
