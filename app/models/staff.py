from sqlalchemy import *
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.database.model import CommonModel


class Staff(CommonModel):
    __tablename__ = "staff"
    name = Column(String(250), nullable=False)
    code = Column(String(50), nullable=False, index=True)
    email = Column(String(250))
    address = Column(String(250))
    phone_number = Column(String(50))
    gender = Column(Integer())
    birthday = Column(BigInteger())
    status = Column(String(50))
    created_at = Column(BigInteger())
    account = relationship("Account", back_populates='staff')
    have_account = Column(Boolean())
    position = relationship("Position", back_populates='staff')
    position_id = Column(UUID(as_uuid=True), ForeignKey('position.id'))
    position_name = Column(String(250))
    department = relationship("Department", back_populates='staff')
    department_id = Column(UUID(as_uuid=True), ForeignKey('department.id'))
    department_name = Column(String(250))
    document = relationship('Document', secondary='staff_document', backref='staff', cascade="all")
    work_report = relationship("WorkReport", back_populates='staff')
