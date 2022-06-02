# Python's Libraries
import json

# Own's Libraries
from libs.models.base_rds import RdsModel

# Third-party Libraries
from sqlalchemy import Column
from sqlalchemy import Integer

from libs.sources.rds_declarative import Base


class SupplierModel(Base, RdsModel):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, nullable=True)
    invoice_address_id = Column(Integer, nullable=False)

    def __repr__(self):
        value = f"SupplierModel: {self.get_Dict()}"
        return value
