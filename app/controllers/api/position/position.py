import traceback

from fastapi import Depends
from typing import Optional
from pydantic import BaseModel
from app.controllers.core.utils.data.convert import format_data
from app.database import get_db
from sqlalchemy.orm import Session
from gatco_restapi.helpers import to_dict

from app.models.position import Position

from app.controllers.api.position import router

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.utils import pagination
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.check import (
    string_is_null_or_empty,
    string_is_not_valid_uuid
)

URL_API = "/position-management"
URL_API_ID = "/position-management/{id}"
URL_LIST = "/position-list/"


class SchemaPosition(BaseModel):
    name: str
    parent_id: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


@router.post(URL_API, dependencies=[Depends(JWTBearer)])
async def create_position(position: SchemaPosition, db: Session = Depends(get_db)):

    if string_is_null_or_empty(position.name):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên chức vụ trống",
                                  response_http_code=400)

    record_position = db.query(Position).filter(
        Position.name == position.name).filter(
        Position.deleted == False).first()

    if record_position:
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": chức vụ đã tồn tại",
                                  response_http_code=400)

    try:
        record_position = Position()

        if position.parent_id:
            record_parent_position = db.query(Position).filter(
                Position.id == position.parent_id).filter(
                Position.deleted == False).first()

            record_position.parent_id = record_parent_position.id

        record_position.name = position.name
        record_position.description = position.description

        db.add(record_position)
        db.commit()

        return format_data_return(response_data={'data': {
                                                    'result': to_dict(record_position)
                                                }},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.put(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def update_position(id, position: SchemaPosition, db: Session = Depends(get_db)):

    if string_is_not_valid_uuid(id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id chức vụ không hợp lệ",
                                  response_http_code=400)

    if string_is_null_or_empty(position.name):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên chức vụ tạo trống",
                                  response_http_code=400)

    record_position = db.query(Position).filter(
        Position.id == id).filter(
        Position.deleted == False).first()

    if not record_position:
        return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy chức vụ",
                                  response_http_code=404)

    record_position_name = db.query(Position).filter(
        Position.id != id).filter(
        Position.name == position.name).filter(
        Position.deleted == False).first()

    if record_position_name:
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": chức vụ đã tồn tại",
                                  response_http_code=400)

    try:
        if position.parent_id:
            record_position_parent = db.query(Position).filter(
                Position.id == position.parent_id).filter(
                Position.deleted == False).first()

            record_position.parent_id = record_position_parent.id

        record_position.name = position.name
        record_position.description = position.description

        db.commit()

        return format_data_return(response_data={'data': {
            'result': to_dict(record_position)
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API, dependencies=[Depends(JWTBearer)])
async def get_position(db: Session = Depends(get_db),  results_per_page: Optional[int] = 10, page: Optional[int] = 1):
    try:
        records_position = db.query(Position).filter(
            Position.deleted == False).all()

        list_data_return = pagination(records_position, results_per_page, page)

        return format_data_return(response_data={'data': list_data_return},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def get_position_id(id, db: Session = Depends(get_db)):
    if string_is_not_valid_uuid(id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id chức vụ không hợp lệ",
                                  response_http_code=400)

    try:

        record_position = db.query(Position).filter(
            Position.id == id).filter(
            Position.deleted == False).first()

        if not record_position:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy chức vụ hợp lệ",
                                      response_http_code=404)

        return format_data_return(response_data={'data': {
            'result': to_dict(record_position)
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.delete(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def delete_position(id, db: Session = Depends(get_db)):

    if string_is_not_valid_uuid(id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id chức vụ không hợp lệ",
                                  response_http_code=400)

    record_position = db.query(Position).filter(
        Position.id == id).filter(
        Position.deleted == False).first()

    try:
        record_position.deleted = True

        db.commit()

        return format_data_return(response_data={'data': {}},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_LIST, dependencies=[Depends(JWTBearer)])
async def get_position_list(id: Optional[str], db: Session = Depends(get_db)):
    if id and string_is_not_valid_uuid(id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id chức vụ không hợp lệ",
                                  response_http_code=400)
    try:
        records_position = db.query(Position).filter(
            Position.id != id if id is not None else True).filter(
            Position.deleted == False).all()

        if not records_position:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy chức vụ hợp lệ",
                                      response_http_code=404)

        list_data_return = [format_data(x) for x in records_position]

        return format_data_return(response_data={'data': {
            'result': list_data_return
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
