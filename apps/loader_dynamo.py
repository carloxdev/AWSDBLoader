from libs.sources.dynamodb_source import DynamoDBSource


def loader_dynamo(_model, _data, _clean_first=False):
    source = DynamoDBSource()
    table_name = _model.__tablename__

    if _clean_first:
        deleted_count = 0
        data_list = source.select_ManyWithScan(table_name)
        print(f"{len(data_list)} records to delete found")
        for data in data_list['Items']:
            source.delete_One(table_name, {"id": data['id']})
            deleted_count += 1
            print(f"Record deleted: {data}")

        print(f"{deleted_count} records were deleted")

    added_count = 0
    for item in _data:
        model = _model.__class__()
        model.fill(item)

        source.insert_One(model)
        added_count += 1
        print(f"Record Added: {model}")

    print(f"{added_count} records were added")
