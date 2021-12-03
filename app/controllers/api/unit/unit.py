import traceback

from fastapi import Depends
from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from unidecode import unidecode
from sqlalchemy.orm import Session
from gatco_restapi.helpers import to_dict

from app.models.unit import Unit

from app.controllers.api.unit import router

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.utils import pagination
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.database.sqlalchemy_function import Unaccent
from app.controllers.core.utils.data.check import (
    string_is_not_null_and_not_empty,
    string_is_null_or_empty,
    string_is_not_valid_uuid
)

URL_API = "/unit-management"
URL_API_ID = "/unit-management/{id}"


class SchemaUnit(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


@router.post(URL_API, dependencies=[Depends(JWTBearer)])
async def create_unit(unit: SchemaUnit, db: Session = Depends(get_db)):
    if string_is_null_or_empty(unit.name):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên đơn vị phát hành trống",
                                  response_http_code=400)

    record_unit = db.query(Unit).filter(
        Unit.name == unit.name).filter(
        Unit.deleted == False).first()

    if record_unit:
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": đơn vị đã tồn tại",
                                  response_http_code=400)

    try:
        record_unit = Unit()

        record_unit.name = unit.name
        record_unit.description = unit.description

        db.add(record_unit)
        db.commit()

        return format_data_return(response_data={'data': {
                                                    'result': to_dict(record_unit)
                                                }},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.put(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def update_unit(id, unit: SchemaUnit, db: Session = Depends(get_db)):

    if string_is_not_valid_uuid(id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id đơn vị phát hành không hợp lệ",
                                  response_http_code=400)

    if string_is_null_or_empty(unit.name):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên đơn vị trống",
                                  response_http_code=400)

    record_unit = db.query(Unit).filter(
        Unit.id == id).filter(
        Unit.deleted == False).first()

    if not record_unit:
        return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy phòng ban",
                                  response_http_code=404)

    elif record_unit.name != unit.name:
        record_unit_name = db.query(Unit).filter(
            Unit.id != id).filter(
            Unit.name == unit.name).filter(
            Unit.deleted == False).first()

        if record_unit_name:
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên đơn vị đã tồn tại",
                                      response_http_code=400)

    try:

        record_unit.name = unit.name
        record_unit.description = unit.description

        db.commit()

        return format_data_return(response_data={'data': {
            'result': to_dict(record_unit)
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API, dependencies=[Depends(JWTBearer)])
async def get_unit(name: Optional[str] = None, db: Session = Depends(get_db), results_per_page: Optional[int] = 10, page: Optional[int] = 1):
    try:
        name_str_unaccent = "%" + unidecode(name.strip().lower()) + "%" if string_is_not_null_and_not_empty(
            name) else None

        records_unit = db.query(Unit).filter(
            Unit.deleted == False).filter(
            Unaccent(Unit.name).ilike(name_str_unaccent)
            if name_str_unaccent is not None else True).order_by(
            Unit.created_at.desc(), Unit.id.desc()).all()

        list_data_return = pagination(records_unit, results_per_page, page)

        return format_data_return(response_data={'data': list_data_return},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def get_unit_id(id, db: Session = Depends(get_db)):
    if string_is_not_valid_uuid(id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id đơn vị không hợp lệ",
                                  response_http_code=400)

    try:

        record_unit = db.query(Unit).filter(
            Unit.id == id).filter(
            Unit.deleted == False).first()

        if not record_unit:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy đơn vị hợp lệ",
                                      response_http_code=404)

        return format_data_return(response_data={'data': {
            'result': to_dict(record_unit)
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.delete(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def delete_unit(id, db: Session = Depends(get_db)):

    if string_is_not_valid_uuid(id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id đơn vị không hợp lệ",
                                  response_http_code=400)

    record_unit = db.query(Unit).filter(
        Unit.id == id).filter(
        Unit.deleted == False).first()

    try:
        record_unit.deleted = True

        db.commit()

        return format_data_return(response_data={'data': {}},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
