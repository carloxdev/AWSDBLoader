import os

from libs.sources.rds_source import RdsCredential
from libs.sources.rds_source import RdsSource
from libs.sources.rds_source import RdsType


def loader_rds(_model, _data):
    credential_obj = RdsCredential(
        _type=RdsType.AURORA_SERVERLESS,
        _db_name=os.environ.get("rds_db_name"),
        _cluster_arn=os.environ.get("cluster_arn"),
        _secret_arn=os.environ.get("secret_arn")
    )

    cont = 0
    source = RdsSource(credential_obj)
    for item in _data:
        model = _model.__class__()
        model.fill(item)

        source.insert(model)
        cont += 1
        print(f"Record Added: {model}")

    print(f"{cont} records were added")
