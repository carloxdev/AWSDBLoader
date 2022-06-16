# Python's Libraries
import os

# Third-party Libraries
from unittest import TestCase
from dotenv import load_dotenv

# Own's Libraries
from apps.loader_dynamo import loader_dynamo
from models.suppplier_model import SupplierInvoicesModel
from data.supplier_data import SUPPLIER_LOCAL_DATA

load_dotenv()

environment = os.environ.get('environment')
print(f"Working with environtment: {environment}")


class SupplierLocalLoaderTest(TestCase):

    def test_When_Success(self):
        loader_dynamo(
            SupplierInvoicesModel(),
            SUPPLIER_LOCAL_DATA,
            environment,
            _clean_first=True,
            _key_fields=['id'],
        )
