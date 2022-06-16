# Python's Libraries
import os

# Third-party Libraries
from unittest import TestCase
from dotenv import load_dotenv

# Own's Libraries
from apps.loader_rds import loader_rds
from models.eisupplier_model import EISupplierModel
from data.eisupplier_data import EISUPPLIER_DATA

load_dotenv()

environment = os.environ.get('environment')
print(f"Working with environtment: {environment}")
print(f"DB Name: {os.environ.get('rds_db_name')}")
print(f"ClusterARN: {os.environ.get('cluster_arn')}")
print(f"SecretARN: {os.environ.get('secret_arn')}")


class EISupplierLoaderTest(TestCase):

    def test_When_Success(self):
        loader_rds(EISupplierModel(), EISUPPLIER_DATA)
