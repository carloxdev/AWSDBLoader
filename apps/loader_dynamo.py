import os

from libs.sources.dynamodb_source import DynamoDBSource


def loader_dynamo(_model, _data):
    cont = 0
    source = DynamoDBSource()

    for item in _data:
        model = _model.__class__()
        model.fill(item)

        source.insert_One(model)
        cont += 1
        print(f"Record Added: {_model}")

    print(f"{cont} records were added")
