# Python's Libraries
import logging

# Third-party Libraries
import boto3
from botocore.exceptions import NoCredentialsError

# Own's Libraries
from libs.errors.source_error import SourceError
from libs.errors.source_error import NoRecordFoundError
from libs.errors.source_error import NoRecordsFoundError


class DynamoDBSource(object):

    def __init__(self, _logger=None, _url=None):
        self.logger = _logger or logging.getLogger(__name__)
        self.client = None
        self.url = _url

    def __connect_WithResource(self):
        try:
            if self.url:
                self.client = boto3.resource(
                    'dynamodb',
                    endpoint_url=self.url
                )
            else:
                self.client = boto3.resource('dynamodb')

            return True

        except NoCredentialsError as e:
            raise SourceError(
                _message="dynamodb wrong credentials",
                _error=str(e),
                _logger=self.logger
            )

        except Exception as e:
            raise SourceError(
                _message=str(e),
                _logger=self.logger,
                _error=str(e)
            )

    def __connect(self):
        try:
            if self.url:
                self.client = boto3.client(
                    'dynamodb',
                    endpoint_url=self.url
                )

            else:
                self.client = boto3.client(
                    'dynamodb'
                )

            return True

        except NoCredentialsError as e:
            raise SourceError(
                _message="dynamodb wrong credentials",
                _error=str(e),
                _logger=self.logger
            )

        except Exception as e:
            raise SourceError(
                _message=str(e),
                _logger=self.logger,
                _error=str(e)
            )

    def select_One(self, _table_name, _filter):
        self.__connect_WithResource()

        try:
            table = self.client.Table(_table_name)
            response = table.get_item(
                Key=_filter
            )

        except Exception as e:
            raise SourceError(
                _message=str(e),
                _error=str(e),
                _logger=self.logger
            )

        data = {}
        if 'Item' in response:
            data = response['Item']

        else:
            raise NoRecordFoundError(
                _message="No record found",
                _logger=self.logger
            )

        print(data)
        return data

    def select_Many(
        self,
        _model,
        _keyconditions,
        _keyconditions_values,
        _attributes_names=None,
        _filters=None,
        _index_name=None,
        _start_key=None,
        _page_size=None
    ):
        self.logger.info(f"<--- Query in table: {_model.__tablename__}")
        if _keyconditions is None or _keyconditions_values is None:
            raise SourceError(
                _message="KeyConditionExpression is missing",
                _error=None,
                _logger=self.logger
            )

        arguments = {}
        arguments['TableName'] = _model.__tablename__
        arguments['KeyConditionExpression'] = _keyconditions
        arguments['ExpressionAttributeValues'] = _keyconditions_values

        if _page_size:
            arguments['PaginationConfig'] = {
                'PageSize': _page_size,
                'StartingToken': None
            }

        if _index_name:
            arguments['IndexName'] = _index_name

        if _filters:
            arguments['FilterExpression'] = _filters

        if _attributes_names:
            arguments['ExpressionAttributeNames'] = _attributes_names

        if _start_key:
            arguments['ExclusiveStartKey'] = _start_key

        try:
            self.__connect()
            paginator = self.client.get_paginator('query')

            self.logger.info(f"Using arguments: {arguments}")
            page_iterator = paginator.paginate(**arguments)

            response = {}
            for page in page_iterator:
                response = page
                break

        except Exception as e:
            raise SourceError(
                _message=str(e),
                _error=str(e),
                _logger=self.logger
            )

        if len(response['Items']) == 0:
            raise NoRecordsFoundError(
                _message="No records found",
                _logger=self.logger
            )

        self.logger.info(f"{len(response['Items'])} Records found")
        return response

    def select_ManyWithScan(
        self,
        _table_name,
        _keyconditions=None,
        _keyconditions_values=None,
        _attributes_names=None,
        _index_name=None,
        _start_key=None
    ):
        print(f"<--- Scan in table: {_table_name}")

        arguments = {}
        arguments['TableName'] = _table_name

        if _keyconditions:
            arguments['FilterExpression'] = _keyconditions
            arguments['ExpressionAttributeValues'] = _keyconditions_values

        if _index_name:
            arguments['IndexName'] = _index_name

        if _attributes_names:
            arguments['ExpressionAttributeNames'] = _attributes_names

        if _start_key:
            arguments['ExclusiveStartKey'] = _start_key

        try:
            self.__connect()
            paginator = self.client.get_paginator('scan')

            print("Using this arguments .......")
            print(arguments)
            page_iterator = paginator.paginate(**arguments)

            data = []
            first = True
            last_evalued = None
            count = 0

            for page in page_iterator:
                count += 1
                print(f"{len(page['Items'])} Records found in page {count}")

                if first:
                    data = page['Items']
                    first = False

                else:
                    data += page['Items']

            print(f"Records found in {count} request: {len(data)}")

        except Exception as e:
            raise SourceError(
                _message=str(e),
                _error=str(e),
                _logger=self.logger
            )

        if len(data) == 0:
            raise NoRecordsFoundError(
                _message="No records found",
                _logger=self.logger
            )

        return_data = {}
        return_data['Items'] = data
        return_data['LastEvaluatedKey'] = last_evalued

        return return_data

    def delete_One(self, _table_name, _filter):
        self.__connect_WithResource()

        try:
            print(f"Table: {_table_name}")
            print(f"With filter: {_filter}")
            table = self.client.Table(_table_name)
            response = table.delete_item(
                Key=_filter
            )

            print(f"Delete Item succeeded: {response}")
            return True

        except Exception as e:
            raise SourceError(
                _message=str(e),
                _error=str(e),
                _logger=self.logger
            )

    def insert_One(self, _table_name, _data):
        print(f"Loading Item in table: {_table_name}")
        self.__connect_WithResource()

        try:
            table = self.client.Table(_table_name)
            table.put_item(Item=_data)

        except Exception as e:
            raise SourceError(
                _message=str(e),
                _error=str(e),
                _logger=self.logger
            )
