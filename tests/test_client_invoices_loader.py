# Python's Libraries
import os

# Third-party Libraries
from unittest import TestCase
from dotenv import load_dotenv

# Own's Libraries
from apps.loader_dynamo import loader_dynamo
from models.client_model import ClientInvoicesModel
from data.client_data import CLIENT_LOCAL_DATA

load_dotenv()

environment = os.environ.get('environment')
print(f"Working with environtment: {environment}")


class ClientLocalLoaderTest(TestCase):

    def test_When_Success(self):
        loader_dynamo(
            ClientInvoicesModel(),
            CLIENT_LOCAL_DATA,
            environment,
            _clean_first=False,
            _key_fields=['id'],
        )
