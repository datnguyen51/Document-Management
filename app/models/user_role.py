from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.database.model import CommonModel


class UserRole(CommonModel):
    __tablename__ = "user_role"
    name = Column(String(50), nullable=False, index=True)
    description = Column(String(250))
    slug = Column(String())
    account = relationship("Account", back_populates="user_role")
    permission = relationship('Permission', secondary='user_role_permission', backref='user_role', cascade="all")
