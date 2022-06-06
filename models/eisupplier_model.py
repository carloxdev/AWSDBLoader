# Third-party Libraries
from sqlalchemy import Column
from sqlalchemy import Integer

# Own's Libraries
from libs.models.base_rds import RdsModel
from libs.sources.rds_declarative import Base


class EISupplierModel(Base, RdsModel):
    __tablename__ = "exporter_importer_supplier"

    exporter_importer_id = Column(Integer, primary_key=True, nullable=True)
    supplier_id = Column(Integer, primary_key=True, nullable=True)

    def __repr__(self):
        value = f"EISupplierModel: {self.get_Dict()}"
        return value
