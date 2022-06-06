# Third-party Libraries
from unittest import TestCase

from apps.loader_rds import loader_rds
from models.suppplier_model import SupplierModel
from data.supplier_data import SUPPLIER_DATA

# Third-party Libraries
from dotenv import load_dotenv

load_dotenv()


# class SupplierLoaderTest(TestCase):

#     def test_When_Success(self):
#         loader_rds(SupplierModel(), SUPPLIER_DATA)
