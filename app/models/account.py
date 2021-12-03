from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.database.model import CommonModel


class Account(CommonModel):
    __tablename__ = 'account'
    username = Column(String(255), nullable=False, index=True, unique=True)
    password = Column(String(), nullable=False, index=True)
    active = Column(Boolean(), default=False)
    user_role = relationship("UserRole", back_populates="account")
    role_id = Column(UUID(as_uuid=True), ForeignKey('user_role.id'))
    staff = relationship("Staff", back_populates="account")
    staff_id = Column(UUID(as_uuid=True), ForeignKey('staff.id'))
