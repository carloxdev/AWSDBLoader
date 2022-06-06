# Third-party Libraries
from unittest import TestCase
from dotenv import load_dotenv

# Own's Libraries
from apps.loader_rds import loader_rds
from models.eisupplier_model import EISupplierModel
from data.eisupplier_data import EISUPPLIER_DATA

load_dotenv()


# class EISupplierLoaderTest(TestCase):

#     def test_When_Success(self):
#         loader_rds(EISupplierModel(), EISUPPLIER_DATA)
