# Third-party Libraries
from unittest import TestCase
from dotenv import load_dotenv

# Own's Libraries
from apps.loader_dynamo import loader_dynamo
from models.suppplier_model import SupplierInvoicesModel
from data.supplier_data import SUPPLIER_LOCAL_DATA

load_dotenv()


class SupplierLocalLoaderTest(TestCase):

    def test_When_Success(self):
        loader_dynamo(SupplierInvoicesModel(), SUPPLIER_LOCAL_DATA, _clean_first=True)
