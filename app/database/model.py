import uuid
import time
from math import floor
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (Column, Boolean, event, BigInteger, String)

from app.database import Base


def default_uuid():
    return str(uuid.uuid4())


def model_oncreate_listener(mapper, connection, instance):
    if instance.created_at is None:
        instance.created_at = floor(time.time())
    if instance.updated_at is None:
        instance.updated_at = floor(time.time())


def model_onupdate_listener(mapper, connection, instance):
    instance.created_at = instance.created_at
    instance.updated_at = floor(time.time())
    if instance.deleted is True:
        instance.deleted_at = floor(time.time())


def adjacency_model_oncreate_listener(mapper, connection, instance):
    pass


def adjacency_model_onupdate_listener(mapper, connection, instance):
    children = instance.children_ids()
    if instance.parent_id in children:
        pass


def adjacency_model_ondelete_listener(mapper, connection, instance):
    children = instance.children_ids()
    if len(children) > 1:
        pass


class CommonModel(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
    created_at = Column(BigInteger(), index=True)
    created_by = Column(String(), nullable=True)
    updated_at = Column(BigInteger())
    updated_by = Column(String(), nullable=True)
    deleted = Column(Boolean(), default=False, index=True)
    deleted_at = Column(BigInteger())
    deleted_by = Column(String(), nullable=True)


event.listen(CommonModel, 'before_insert',
             model_oncreate_listener, propagate=True)
event.listen(CommonModel, 'before_update',
             model_onupdate_listener, propagate=True)


class CommonAdjacencyModel(CommonModel):
    __abstract__ = True

    def __todict__(self):
        return {"id": self.id}

    def dump(self, _indent=0):
        obj = self.__todict__()
        obj["children"] = [c.dump() for c in self.children.values()]
        return obj

    def _children_ids(self, data):
        if type(data) is list:
            data.append(self.id)
            for r in self.children.values():
                r._children_ids(data)

    def children_ids(self):
        data = []
        self._children_ids(data)
        return data


event.listen(CommonAdjacencyModel, 'before_insert',
             adjacency_model_oncreate_listener, propagate=True)
event.listen(CommonAdjacencyModel, 'before_update',
             adjacency_model_onupdate_listener, propagate=True)
event.listen(CommonAdjacencyModel, 'before_delete',
             adjacency_model_ondelete_listener, propagate=True)
