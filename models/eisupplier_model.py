
# Own's Libraries
from libs.models.base_rds import RdsModel

# Third-party Libraries
from sqlalchemy import Column
from sqlalchemy import Integer

from libs.sources.rds_declarative import Base


class EISupplierModel(Base, RdsModel):
    __tablename__ = "importer_exporter_supplier"

    importer_exporter_id = Column(Integer, primary_key=True, nullable=True)
    supplier_id = Column(Integer, primary_key=True, nullable=True)

    def __repr__(self):
        value = f"EISupplierModel: {self.get_Dict()}"
        return value
