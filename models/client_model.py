
from libs.models.base_dynamo import DynamoModel
from libs.models.base_dynamo import NumberAttr
from libs.models.base_dynamo import BoolenaAttr


class ClientDynamoModel(DynamoModel):

    def __init__(
        self,
        _id=None,
        _importer=None,
        _exporter=None,
        _invoice_tolerance_total=None,
        _invoice_tolerance_detail=None,
        _company_id=None
    ):
        self.id = NumberAttr(_id)
        self.importer = BoolenaAttr(_importer)
        self.exporter = BoolenaAttr(_exporter)
        self.invoice_tolerance_total = NumberAttr(_invoice_tolerance_total)
        self.invoice_tolerance_detail = NumberAttr(_invoice_tolerance_detail)
        self.company_id = NumberAttr(_company_id)

    def __repr__(self):
        value = f"ClientModel: {self.get_Dict()}"
        return value


class ClientInvoicesModel(ClientDynamoModel):
    __tablename__ = "nvs-bts-us-va-invoices-client"
