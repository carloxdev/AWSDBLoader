# Python's Libraries
import json
from datetime import datetime

# Third-party Libraries
from sqlalchemy.orm.collections import InstrumentedList


class RdsModel(object):

    def backref_ToDic(self, _value, _signer=None):
        data = []
        for item in _value:
            item_dict = item.get_Dict(
                _relations=False,
                _signer=_signer
            )
            data.append(item_dict)

        return data

    def get_Dict(
        self,
        _nulls=True,
        _primaries=True,
        _relations=False,
        _backref=False,
        _except_rel=[],
        _signer=None
    ):
        data = {}

        for attr, column in self.__mapper__.c.items():
            if _primaries is False and column.primary_key:
                continue

            column_value = getattr(self, attr)
            if _nulls is False and column_value is None:
                continue

            data[column.key] = column_value

        if _relations:
            for attr, relation in self.__mapper__.relationships.items():

                value = getattr(self, attr)

                if value is None and _nulls:
                    data[relation.key] = None
                    continue

                if relation.key in _except_rel:
                    continue

                if type(value) == InstrumentedList:
                    if _backref is False:
                        continue

                    if relation.key in _except_rel:
                        continue

                    if value:
                        data[relation.key] = self.backref_ToDic(
                            _value=value,
                            _signer=_signer
                        )

                    else:
                        data[relation.key] = value

                else:
                    data[relation.key] = value.get_Dict(
                        _nulls=_nulls,
                        _primaries=_primaries,
                        _relations=_relations,
                        _backref=_backref,
                        _except_rel=_except_rel,
                        _signer=_signer
                    )

        return data

    def get_Json(
        self,
        _relations=False,
        _backref=False,
        _except_rel=[],
        _signer=None
    ):

        def extended_encoder(x):
            if isinstance(x, datetime):
                return x.isoformat()

        return json.dumps(
            self.get_Dict(
                _relations=_relations,
                _backref=_backref,
                _except_rel=_except_rel,
                _signer=_signer
            ),
            default=extended_encoder
        )

    def fill(self, _data_dic, _with_type=False):
        attributes = dir(self)

        for key, value in _data_dic.items():
            if key in attributes:
                setattr(self, key, value)

            else:
                raise ValueError(
                    f"The data attribute {key} is not in {self}"
                )


class RdsModelCollection(list):

    def fill(self, _list):
        self.extend(_list)

    def get_Json(self):
        data = []
        for item in self:
            data.append(item.get_Dict())

        return json.dumps(data)


class RdsModelSerializer(object):

    def __init__(self, _data=None, _many=False, _translate=False):
        self.data = _data
        self.many = _many
        self.translate = _translate

        if hasattr(self, "list_attrs") is False:
            raise NameError("list_attrs is not defined")

    def __get_LowerCamelCaseFormat(self, _value):
        new_value = ''.join(x.capitalize() or '_' for x in _value.split('_'))
        return new_value[0].lower() + new_value[1:]

    def __get_AttrToEval(self, _serial_attr):
        if self.translate:
            if 'translate_list' not in dir(self):
                return _serial_attr

            if self.translate_list is None:
                return _serial_attr

            if _serial_attr not in self.translate_list:
                return _serial_attr

            return self.translate_list[_serial_attr]

        else:
            return _serial_attr

    def __get_Label(self, _attr_name):
        if hasattr(self, "labels") is False:
            return None

        if _attr_name in self.labels.keys():
            return self.labels[_attr_name]
        else:
            return None

    def __get_ItemDict(self, _item):
        data = {}
        class_attrs = _item.__dict__.keys()

        for serial_attr in self.list_attrs:
            serial_attr_eval = self.__get_AttrToEval(serial_attr)

            if serial_attr_eval not in class_attrs:
                raise NameError(f"{serial_attr_eval} is not in class {_item.__class__}")

            value = getattr(_item, serial_attr_eval)

            attr_label = self.__get_Label(serial_attr)

            if attr_label:
                data[attr_label] = value

            else:
                data[self.__get_LowerCamelCaseFormat(serial_attr)] = value

        return data

    def get_Dict(self):
        if self.many:
            list = []
            for dta in self.data:
                list.append(self.__get_ItemDict(dta))

            return list
        else:
            return self.__get_ItemDict(self.data)

    def get_Json(self):
        json_data = json.dumps(self.get_Dict())
        return json_data
