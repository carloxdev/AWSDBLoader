# Python's Libraries
import os

# Third-party Libraries
from unittest import TestCase

# Third-party Libraries
from dotenv import load_dotenv

# Own's Libraries
from apps.loader_rds import loader_rds
from models.suppplier_model import SupplierModel
from data.supplier_data import SUPPLIER_DATA

load_dotenv()

environment = os.environ.get('environment')
print(f"Working with environtment: {environment}")
print(f"DB Name: {os.environ.get('rds_db_name')}")
print(f"ClusterARN: {os.environ.get('cluster_arn')}")
print(f"SecretARN: {os.environ.get('secret_arn')}")


class SupplierLoaderTest(TestCase):

    def test_When_Success(self):
        loader_rds(SupplierModel(), SUPPLIER_DATA)
