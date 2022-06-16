# Third-party Libraries
from sqlalchemy import Column
from sqlalchemy import Integer

from libs.sources.rds_declarative import Base


# Own's Libraries
from libs.models.base_rds import RdsModel
from libs.models.base_dynamo import DynamoModel
from libs.models.base_dynamo import NumberAttr
from libs.models.base_dynamo import StringAttr
from libs.models.base_dynamo import ArrayAttr


class SupplierModel(Base, RdsModel):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, nullable=True)
    invoice_address_id = Column(Integer, nullable=False)

    def __repr__(self):
        value = f"SupplierModel: {self.get_Dict()}"
        return value


class SupplierDynamoModel(DynamoModel):

    def __init__(
        self,
        _id=None,
        _company_id=None,
        _invoice_address_id=None,
        _op_key=None,
        _exporters_importers=[]
    ):
        self.id = NumberAttr(_id)
        self.company_id = NumberAttr(_company_id)
        self.invoice_address_id = NumberAttr(_invoice_address_id)
        self.op_key = StringAttr(_op_key)
        self.exporters_importers = ArrayAttr(_exporters_importers)

    def __repr__(self):
        value = f"SupplierModel: {self.get_Dict()}"
        return value


class SupplierInvoicesModel(SupplierDynamoModel):
    __tablename__ = "nvs-bts-us-va-invoices-suppliers"


class SupplierTrafficModel(SupplierDynamoModel):
    __tablename__ = "nvs-bts-us-va-traffic-suppliers"