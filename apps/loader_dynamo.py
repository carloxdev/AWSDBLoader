from libs.sources.dynamodb_source import DynamoDBSource


def loader_dynamo(_model, _data, _environment, _clean_first=False, _key_fields=None):
    source = DynamoDBSource()
    table_name = f"{_model.__tablename__}-{_environment[0]}"

    if _clean_first:
        deleted_count = 0
        data_list = source.select_ManyWithScan(table_name)
        print(f"{len(data_list['Items'])} records to delete found")
        for data in data_list['Items']:
            record_model = _model.__class__()
            record_model.fill(data, _with_type=True)

            dict = {}
            for key in _key_fields:
                raw_items = data[key]
                for type, value in raw_items.items():
                    if type == 'N':
                        dict[key] = int(value)

                    if type == 'S':
                        dict[key] = value

            source.delete_One(table_name, dict)
            deleted_count += 1
            print(f"Record deleted: {dict}")

        print(f"{deleted_count} records were deleted")

    added_count = 0
    for item in _data:
        model = _model.__class__()
        model.fill(item)

        source.insert_One(table_name, model.get_Dict())
        added_count += 1
        print(f"Record Added: {model}")

    print(f"{added_count} records were added")
