import traceback

from fastapi import Depends
from typing import Optional
from pydantic import BaseModel
from unidecode import unidecode
from app.database import get_db
from sqlalchemy.orm import Session
from gatco_restapi.helpers import to_dict

from app.models.department import Department

from app.controllers.api.department import router

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.utils import pagination
from app.controllers.core.utils.database.sqlalchemy_function import Unaccent
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.check import (
    string_is_not_null_and_not_empty,
    string_is_null_or_empty,
    string_is_not_valid_uuid
)

URL_API = "/department-management"
URL_API_ID = "/department-management/{id}"


class SchemaDepartment(BaseModel):
    name: str
    created_at: Optional[str] = None
    parent_id: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


@router.post(URL_API, dependencies=[Depends(JWTBearer)])
async def create_department(department: SchemaDepartment, db: Session = Depends(get_db)):

    if string_is_null_or_empty(department.name):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên trống",
                                  response_http_code=400)

    if string_is_null_or_empty(department.parent_id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id phòng ban trực thuộc trống",
                                  response_http_code=400)

    record_department = db.query(Department).filter(
        Department.name == department.name).filter(
        Department.deleted == False).first()

    if record_department:
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": phòng ban đã tồn tại",
                                  response_http_code=400)

    try:
        record_department = Department()

        if department.parent_id:
            record_parent_department = db.query(Department).filter(
                Department.id == department.parent_id).filter(
                Department.deleted == False).first()

            record_department.parent_id = record_parent_department.id

        record_department.name = department.name
        record_department.description = department.description

        if department.created_at:
            record_department.created_at = department.created_at

        db.add(record_department)
        db.commit()

        return format_data_return(response_data={'data': {
                                                    'result': to_dict(record_department)
                                                }},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.put(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def update_department(id, department: SchemaDepartment, db: Session = Depends(get_db)):

    if string_is_not_valid_uuid(id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id phòng ban không hợp lệ",
                                  response_http_code=400)

    if string_is_null_or_empty(department.name):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên phòng ban và ngày tạo trống",
                                  response_http_code=400)

    record_department = db.query(Department).filter(
        Department.id == id).filter(
        Department.deleted == False).first()

    if not record_department:
        return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy phòng ban",
                                  response_http_code=404)

    elif record_department.name != department.name:
        record_department_name = db.query(Department).filter(
            Department.id != id).filter(
            Department.name == department.name).filter(
            Department.deleted == False).first()

        if record_department_name:
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên phòng ban đã tồn tại",
                                      response_http_code=400)

    try:
        if department.parent_id:
            record_parent_department = db.query(Department).filter(
                Department.id == department.parent_id).filter(
                Department.deleted == False).first()

            if record_parent_department:
                record_department.parent_id = record_parent_department.id

        record_department.name = department.name
        if record_department.created_at:
            record_department.created_at = department.created_at
        record_department.description = department.description

        db.commit()

        return format_data_return(response_data={'data': {
                                                    'result': to_dict(record_department)
                                                }},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API, dependencies=[Depends(JWTBearer)])
async def get_department(name: Optional[str] = None, id: Optional[str] = None, db: Session = Depends(get_db), results_per_page: Optional[int] = 10, page: Optional[int] = 1):
    try:
        name_str_unaccent = "%" + unidecode(name.strip().lower()) + "%" if string_is_not_null_and_not_empty(name) else None

        if id:
            records_department = db.query(Department).filter(
                Department.id != id).filter(
                Unaccent(Department.name).ilike(name_str_unaccent)
                if name_str_unaccent is not None else True).filter(
                Department.deleted == False).order_by(
                Department.created_at.desc(), Department.id.desc()).all()
        else:
            records_department = db.query(Department).filter(
                Unaccent(Department.name).ilike(name_str_unaccent)
                if name_str_unaccent is not None else True).filter(
                Department.deleted == False).order_by(
                Department.created_at.desc(), Department.id.desc()).all()

        list_data_return = pagination(records_department, results_per_page, page)

        return format_data_return(response_data={'data': list_data_return},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def get_department_id(id, db: Session = Depends(get_db)):
    if string_is_not_valid_uuid(id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id phòng ban không hợp lệ",
                                  response_http_code=400)

    try:

        record_department = db.query(Department).filter(
            Department.id == id).filter(
            Department.deleted == False).first()

        if not record_department:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy phòng ban hợp lệ",
                                      response_http_code=404)

        return format_data_return(response_data={'data': {
                                                    'result': to_dict(record_department)
                                                }},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.delete(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def delete_department(id, db: Session = Depends(get_db)):

    if string_is_not_valid_uuid(id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id phòng ban không hợp lệ",
                                  response_http_code=400)

    record_department = db.query(Department).filter(
        Department.id == id).filter(
        Department.deleted == False).first()

    try:
        record_department.deleted = True

        db.commit()

        return format_data_return(response_data={'data': {}},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
