# Python's Libraries
import logging
import copy
from enum import Enum

# Third-party Libraries
from sqlalchemy import create_engine
from sqlalchemy import MetaData

from sqlalchemy import desc
from sqlalchemy import asc

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import StatementError

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

# from sqlalchemy.orm.collections import InstrumentedList

from sqlalchemy_pagination import paginate

# Own's Libraries
from libs.errors.source_error import SourceError
from libs.errors.source_error import NoRecordFoundError
from libs.errors.source_error import NoRecordsFoundError
from libs.errors.source_error import MultipleRecordsFoundError
from libs.utils.decorators import step


class JoinType(Enum):
    JOIN = "join"
    OUTER = "outerjoin"


class RdsType(Enum):
    AURORA_REGULAR = "AURORA_REGULAR"
    AURORA_SERVERLESS = "AURORA_SERVERLESS"

    @staticmethod
    def list():
        return list(map(lambda item: item.value, RdsType))


class RdsCredential(object):

    def __init__(
        self,
        _type,
        _db_name,
        _user=None,
        _password=None,
        _host=None,
        _port=None,
        _cluster_arn=None,
        _secret_arn=None,
    ):
        self.type = _type
        self.db_name = _db_name
        self.user = _user
        self.password = _password
        self.host = _host if _host else "localhost"
        self.port = _port if _port else 3306
        self.cluster_arn = _cluster_arn
        self.secret_arn = _secret_arn


class RdsSource(object):
    """Object with methods that help with the DB operations"""

    def __init__(self, _credential_obj, _logger=None):
        self.engine = None

        self.credential_obj = _credential_obj
        self.session = None
        self.records_per_page = 20
        self.logger = _logger or logging.getLogger(__name__)

    def close_Connection(self):
        if self.session:
            self.logger.info("Closing session")
            self.session.rollback()
            self.session.close()

        if self.engine:
            self.logger.info("Disposing Engine")
            self.engine.dispose()

    def set_Engine(self):
        if self.engine:
            return True

        if self.credential_obj.type.value not in RdsType.list():
            raise SourceError(
                _message="No RdsType was defined!",
                _logger=self.logger
            )

        try:
            if self.credential_obj.type == RdsType.AURORA_REGULAR:
                URL_CONNECTION = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
                    self.credential_obj.user,
                    self.credential_obj.password,
                    self.credential_obj.host,
                    self.credential_obj.port,
                    self.credential_obj.db_name
                )
                self.logger.info(f"Building engine with url ...: {URL_CONNECTION}")
                self.engine = create_engine(URL_CONNECTION)

            elif self.credential_obj.type == RdsType.AURORA_SERVERLESS:
                URL_CONNECTION = f'mysql+auroradataapi://:@/{self.credential_obj.db_name}'
                self.logger.info(f"Building engine with url ...: {URL_CONNECTION}")
                self.logger.info(f"And Cluster ARN: {self.credential_obj.cluster_arn}")
                self.logger.info(f"And Secrt Store ARN: {self.credential_obj.secret_arn}")
                self.engine = create_engine(
                    URL_CONNECTION,
                    echo=False,
                    connect_args=dict(
                        aurora_cluster_arn=self.credential_obj.cluster_arn,
                        secret_arn=self.credential_obj.secret_arn
                    )
                )
                self.logger.info("Connection success!!")

            else:
                raise SourceError(
                    _message=f"Connection don't defined for type {self.credential_obj.type}",
                    _logger=self.logger
                )

            Session = sessionmaker(bind=self.engine)
            self.session = Session()

            return True

        except StatementError as e:
            print(str(e))
            self.close_Connection()
            raise SourceError(
                _message="Aurora not up yet, retry",
                _logger=self.logger
            )

        except Exception as e:
            self.close_Connection()
            raise SourceError(
                _message=str(e),
                _logger=self.logger
            )

    def get_Tables(self):
        self.logger.info("Getting tables...")
        self.set_Engine()
        try:
            metadata_obj = MetaData()
            metadata_obj.reflect(self.engine)
            return list(metadata_obj.tables.keys())

        except Exception as e:
            raise SourceError(
                _message=str(e),
                _logger=self.logger
            )

    def create_Table(self, _model):
        self.logger.info(f"Creating table...: {_model.__tablename__}")
        self.set_Engine()

        try:
            _model.__table__.create(self.engine)

        except Exception as e:
            raise SourceError(
                _message=str(e),
                _logger=self.logger
            )

    def select_One(self, _model):
        """Search for a record from the attributes of a model
        :param _model: Object of type Model to be search
        :type _model: Model
        :raises SourceError: When fail some validation
        :raises NoRecordFoundError: When the record is not found
        :raises MultipleRecordsFoundError: When more than one record is found
        :return: Object of type Model
        :rtype: Model
        """
        self.logger.info(
            f'Searching in table...: {_model.__table__}'
        )

        self.set_Engine()

        filters = _model.get_Dict(_nulls=False)

        if bool(filters) is False:
            raise SourceError(
                _message="No value was specified in any attribute.",
                _logger=self.logger
            )

        try:
            query = self.session.query(_model.__class__)
            for key in filters.keys():
                query = query.filter(
                    getattr(_model.__class__, key) == filters[key]
                )

            record = query.one()
            return record

        except NoResultFound:
            self.close_Connection()
            msg = "Record not found"
            raise NoRecordFoundError(
                _message=msg,
                _error=msg,
                _logger=self.logger
            )

        except MultipleResultsFound:
            self.close_Connection()
            msg = "There is more than one record"
            raise MultipleRecordsFoundError(
                _message=msg,
                _error=msg,
                _logger=self.logger
            )

        except StatementError as e:
            self.close_Connection()
            if "Communications link failure" in e.args[0]:
                raise SourceError(
                    "Something went wrong while connecting to Aurora Serverless, "
                    "please retry in a few minutes and if the problem persists, "
                    "contact Admin Support.",
                    _error="DB_CONNECTION_NO_AVAILABLE"
                )
            else:
                raise SourceError(e.args[0])

        except Exception as e:
            self.close_Connection()
            raise SourceError(
                _message=str(e),
                _error=str(e),
                _logger=self.logger
            )

    def select_Many(
        self,
        _model,
        _custom_filters=None,
        _order_column=None,
        _arrange="asc",
        _limit=10,
        _page=1
    ):
        self.logger.info(f'Searching in table...: {_model.__table__}')
        self.set_Engine()

        try:
            self.logger.info("Build filters!!")
            if _custom_filters is not None:
                query = self.session.query(_model.__class__)
                query = query.filter(_custom_filters)

            else:
                filters = _model.get_Dict(_nulls=False)

                if bool(filters) is False:
                    query = self.session.query(_model.__class__)

                else:
                    query = self.session.query(_model.__class__)
                    for key in filters.keys():
                        query = query.filter(
                            getattr(_model.__class__, key) == filters[key]
                        )

            records = None
            self.records_per_page = _limit
            if _order_column:
                if _arrange == "asc":
                    page = paginate(
                        query.order_by(asc(_order_column)),
                        _page,
                        self.records_per_page
                    )
                else:
                    page = paginate(
                        query.order_by(desc(_order_column)),
                        _page,
                        self.records_per_page
                    )

            else:
                page = paginate(
                    query,
                    _page,
                    self.records_per_page
                )

            records = page.items
            next_page = page.next_page
            self.logger.info(f"Qty pages: {page.pages}")
            self.logger.info(f"Next page: {page.next_page}")

        except StatementError as e:
            self.close_Connection()
            if "Communications link failure" in e.args[0]:
                raise SourceError(
                    "Something went wrong while connecting to Aurora Serverless, "
                    "please retry in a few minutes and if the problem persists, "
                    "contact Admin Support.",
                    _error="DB_CONNECTION_NO_AVAILABLE"
                )
            else:
                raise SourceError(e.args[0])

        except Exception as e:
            self.close_Connection()
            raise SourceError(
                _message=str(e),
                _source="RdsSource.select_Many"
            )

        qty_records = len(records)
        if qty_records == 0:
            msg = 'No records found'
            raise NoRecordsFoundError(
                _message=msg,
                _error=msg,
                _source="RdsSource.select_Many"
            )

        print(f'{qty_records} records found')
        return records, next_page

    def calculate_Offset(self, _page, _limit):
        return (_page - 1) * _limit

    def select_Many_ByQuery(self, _model, _query):
        self.set_Engine()

        if _query is None:
            raise SourceError(
                _message="_query param is None",
                _logger=self.logger
            )

        filters = _model.get_Dict(_nulls=False)

        try:
            query = self.session.execute(_query, filters)
            records = query.fetchall()

        except StatementError as e:
            self.close_Connection()
            if "Communications link failure" in e.args[0]:
                raise SourceError(
                    "Something went wrong while connecting to Aurora Serverless, "
                    "please retry in a few minutes and if the problem persists, "
                    "contact Admin Support.",
                    _error="DB_CONNECTION_NO_AVAILABLE"
                )
            else:
                raise SourceError(e.args[0])

        except Exception as e:
            self.session.rollback()
            raise SourceError(
                _message=str(e),
                _logger=self.logger
            )

        qty_records = len(records)

        if qty_records == 0:
            raise NoRecordsFoundError(
                _message='Records not found',
                _logger=self.logger
            )

        record_list = []

        for record in records:
            index = 0
            model_item = copy.deepcopy(_model)
            for column_name in query.keys():
                setattr(model_item, column_name, record[index])
                index += 1

            record_list.append(model_item)

        self.logger.info(f'{qty_records} Records found')
        return record_list

    def select_Many_With_Custom_Joins(
        self,
        _model,
        _custom_filters=None,
        _custom_query=None,
        _custom_join=None,
        _order_column=None,
        _arrange="asc",
        _limit=10,
        _page=1
    ):
        self.set_Engine()
        try:
            if _custom_query is not None:
                query = self.session.query(_model.__class__.id, _model.__class__.name, _custom_query).distinct()
            else:
                query = self.session.query(_model.__class__)

            if _custom_join is not None:
                query = query.outerjoin(_custom_join)

            if _custom_filters is not None:
                query = query.filter(_custom_filters)

            records = None
            self.records_per_page = _limit

            if _order_column:
                if _arrange == "asc":
                    page = paginate(
                        query.order_by(asc(_model.__class__.name)),
                        _page,
                        self.records_per_page
                    )
                else:
                    page = paginate(
                        query.order_by(desc(_model.__class__.name)),
                        _page,
                        self.records_per_page
                    )

            else:
                page = paginate(
                    query,
                    _page,
                    self.records_per_page
                )

            records = page.items
            next_page = page.next_page

        except StatementError as e:
            self.close_Connection()
            if "Communications link failure" in e.args[0]:
                raise SourceError(
                    "Something went wrong while connecting to Aurora Serverless, "
                    "please retry in a few minutes and if the problem persists, "
                    "contact Admin Support.",
                    _error="DB_CONNECTION_NO_AVAILABLE"
                )
            else:
                raise SourceError(e.args[0])

        except Exception as e:
            self.close_Connection()
            raise SourceError(
                _message=str(e),
                _source="RdsSource.select_Many",
                _logger=self.logger
            )

        qty_records = len(records)
        if qty_records == 0:
            msg = 'No records found'
            raise NoRecordsFoundError(
                _message=msg,
                _error=msg,
                _source="RdsSource.select_Many",
                _logger=self.logger
            )

        self.logger.info(f'{qty_records} records found')
        return records, next_page

    def insert(self, _model):
        """Inserta un registro en la BD a partir de un modelo.

        :param _model: Instancia de tipo Model con los datos a insertar.
        :type _model: Model
        :raises DataBaseValidationError: Cuando no pase alguna de las validaciones.
        :return: True en caso de que la operacion finalize correctamente.
        :rtype: bool
        """
        self.logger.info(f'Insertando en Tabla: {_model.__tablename__}')
        self.set_Engine()

        try:
            self.session.add(_model)
            self.session.flush()
            self.logger.info('Registro insertado con exito.')

        except IntegrityError as e:
            self.close_Connection()
            raise SourceError(
                _message=e._message(),
                _logger=self.logger
            )

        except StatementError as e:
            self.close_Connection()
            if "Communications link failure" in e.args[0]:
                raise SourceError(
                    "Something went wrong while connecting to Aurora Serverless, "
                    "please retry in a few minutes and if the problem persists, "
                    "contact Admin Support.",
                    _error="DB_CONNECTION_NO_AVAILABLE"
                )
            else:
                raise SourceError(e.args[0])

        except Exception as e:
            self.close_Connection()
            raise SourceError(
                _message=str(e),
                _logger=self.logger
            )

        else:
            self.session.commit()
            return True

    def select_ManyWithCustomJoins(
        self,
        _model,
        _model_other=None,
        _custom_filters=None,
        _custom_join=None,
        _order_column=None,
        _arrange="asc",
        _limit=10,
        _page=1
    ):
        self.set_Engine()
        try:
            if _model_other is not None:
                query = self.session.query(_model.__class__, _model_other.__class__)
            else:
                query = self.session.query(_model.__class__)

            if _custom_join is not None:
                query = query.outerjoin(_custom_join)

            if _custom_filters is not None:
                query = query.filter(_custom_filters)

            records = None
            self.records_per_page = _limit

            if _order_column:
                if _arrange == "asc":
                    page = paginate(
                        query.order_by(asc(_model_other.__class__.legal_name)),
                        _page,
                        self.records_per_page
                    )
                else:
                    page = paginate(
                        query.order_by(desc(_model_other.__class__.legal_name)),
                        _page,
                        self.records_per_page
                    )

            else:
                page = paginate(
                    query,
                    _page,
                    self.records_per_page
                )

            records = page.items
            next_page = page.next_page

        except StatementError as e:
            self.close_Connection()
            if "Communications link failure" in e.args[0]:
                raise SourceError(
                    "Something went wrong while connecting to Aurora Serverless, "
                    "please retry in a few minutes and if the problem persists, "
                    "contact Admin Support.",
                    _error="DB_CONNECTION_NO_AVAILABLE"
                )
            else:
                raise SourceError(e.args[0])

        except Exception as e:
            self.close_Connection()
            raise SourceError(
                _message=str(e),
                _source="RdsSource.select_Many",
                _logger=self.logger
            )

        qty_records = len(records)
        if qty_records == 0:
            msg = 'No records found'
            raise NoRecordsFoundError(
                _message=msg,
                _error=msg,
                _source="RdsSource.select_Many",
                _logger=self.logger
            )

        self.logger.info(f'{qty_records} records found')
        return records, next_page

    @step("[SOURCE] Getting Query Object ...")
    def __get_QueryObject(self, _model_name, _join_models, _join_type):
        if _join_models is None:
            query = self.session.query(_model_name)
            return query

        recover_models = _join_models.copy()
        recover_models.insert(0, _model_name)

        query = self.session.query(*recover_models)
        for entity in _join_models:
            query = getattr(query, _join_type.value)(entity)

        return query

    @step("[SOURCE] Setting Filters ...")
    def __set_Filters(self, _model_name, _query, _filters, _custom_filters=None):
        if _custom_filters:
            for filter in _custom_filters:
                _query = _query.filter(filter)

        if bool(_filters):
            for key in _filters.keys():
                _query = _query.filter(getattr(_model_name, key) == _filters[key])

        return _query

    @step("[SOURCE] Get Page object ...")
    def __get_Page(self, _query, _limit, _order_column, _arrange, _page):
        self.records_per_page = _limit

        page_obj = None

        if _order_column:
            page_obj = paginate(
                _query.order_by(locals()[_arrange](_order_column)),
                _page,
                self.records_per_page
            )

        else:
            page_obj = paginate(
                _query,
                _page,
                self.records_per_page
            )

        return page_obj

    @step("[SOURCE] Select Many with Joins ...")
    def select_Many_WithJoins(
        self,
        _model,
        _join_models=None,
        _join_type=JoinType.JOIN,
        _custom_filters=None,
        _order_column=None,
        _arrange="asc",
        _limit=10,
        _page=1
    ):
        self.set_Engine()

        try:
            model_name = _model.__class__
            query = self.__get_QueryObject(model_name, _join_models, _join_type)

            query = self.__set_Filters(
                model_name,
                query,
                _model.get_Dict(_nulls=False),
                _custom_filters
            )

            page = self.__get_Page(query, _limit, _order_column, _arrange, _page)

            records = page.items
            next_page = page.next_page

            self.logger.info(f"Qty pages: {page.pages}")
            self.logger.info(f"Next page: {page.next_page}")

        except StatementError as e:
            self.close_Connection()
            if "Communications link failure" in e.args[0]:
                raise SourceError(
                    "Something went wrong while connecting to Aurora Serverless, "
                    "please retry in a few minutes and if the problem persists, "
                    "contact Admin Support.",
                    _error="DB_CONNECTION_NO_AVAILABLE"
                )
            else:
                raise SourceError(e.args[0])

        except Exception as e:
            self.close_Connection()
            raise SourceError(
                _message=str(e),
                _source="RdsSource.select_Many"
            )

        qty_records = len(records)
        self.logger.info(f"Qty of records founderd: {qty_records}")
        if qty_records == 0:
            msg = 'No records found'
            raise NoRecordsFoundError(
                _message=msg,
                _error=msg,
                _source="RdsSource.select_Many"
            )

        return records, next_page
