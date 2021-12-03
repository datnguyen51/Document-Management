from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.database.model import CommonModel


class UserRolePermission(CommonModel):
    __tablename__ = "user_role_permission"
    user_role_id = Column(UUID(as_uuid=True), ForeignKey('user_role.id'))
    permission_id = Column(UUID(as_uuid=True), ForeignKey('permission.id'))
