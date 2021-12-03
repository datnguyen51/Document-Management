from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.database.model import CommonModel


class WorkReport(CommonModel):
    __tablename__ = 'work_report'
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=False)
    status = Column(String(500), nullable=False)
    review_description = Column(String(500))
    document = relationship("Document", back_populates="work_report")
    document_id = Column(UUID(as_uuid=True), ForeignKey('document.id'))
    document_name = Column(String(250))
    staff = relationship("Staff", back_populates="work_report")
    staff_id = Column(UUID(as_uuid=True), ForeignKey('staff.id'))
    staff_name = Column(String(250))
    staff_code = Column(String(250))
    department = relationship("Department", back_populates="work_report")
    department_id = Column(UUID(as_uuid=True), ForeignKey('department.id'))
    department_name = Column(String(250))
