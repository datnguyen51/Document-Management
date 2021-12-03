from app.models.account import Account
import traceback

from typing import Optional
from pydantic import BaseModel
from unidecode import unidecode
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, Request
from sqlalchemy.sql.elements import or_
from gatco_restapi.helpers import to_dict

from app.models.staff import Staff
from app.models.position import Position
from app.models.department import Department

from app.controllers.core.auth.bearer import JWTBearer
from app.controllers.core.auth.handler import decodeJWT

from app.common.message import ErrorMessage
from app.controllers.core.utils import pagination
from app.controllers.core.client import format_data_return
from app.controllers.api.staff import check_department, data_department, router
from app.controllers.core.utils.database.sqlalchemy_function import Unaccent
from app.controllers.core.utils.data.check import (
    string_is_not_null_and_not_empty,
    string_is_null_or_empty,
    string_is_not_valid_uuid,
    is_valid_email,
)

URL_API = "/staff-management"
URL_API_ID = "/staff-management/{id}"


class SchemaStaff(BaseModel):
    name: str
    code: str
    email: str
    status: Optional[str] = None
    gender: int
    address: str
    birthday: str
    phone_number: str
    department_id: Optional[str] = None
    position_id: Optional[str] = None

    class Config:
        orm_mode = True


@router.post(URL_API, dependencies=[Depends(JWTBearer)])
async def create_staff(staff: SchemaStaff, db: Session = Depends(get_db)):
    try:
        if string_is_null_or_empty(staff.name) or string_is_null_or_empty(staff.code):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": name, code trống",
                                      response_http_code=400)

        if staff.email and not is_valid_email(staff.email):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": email không đúng định dạng",
                                      response_http_code=400)

        record_staff = db.query(Staff).filter(
            Staff.code == staff.code).filter(
            Staff.deleted == False).first()

        if record_staff:
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": code đã tồn tại",
                                      response_http_code=400)

        record_staff = db.query(Staff).filter(
            Staff.email == staff.email).filter(
            Staff.deleted == False).first()

        if record_staff:
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": email đã tồn tại",
                                      response_http_code=400)

        try:
            record_staff = Staff()

            if staff.position_id:
                record_position = db.query(Position).filter(
                    Position.id == staff.position_id).filter(
                    Position.deleted == False).first()

                record_staff.position_id = record_position.id
                record_staff.position_name = record_position.name

            if staff.department_id:
                record_department = db.query(Department).filter(
                    Department.id == staff.department_id).filter(
                    Department.deleted == False).first()

                record_staff.department_id = record_department.id
                record_staff.department_name = record_department.name

            record_staff.name = staff.name
            record_staff.code = staff.code
            record_staff.email = staff.email
            record_staff.address = staff.address
            record_staff.phone_number = staff.phone_number
            record_staff.gender = staff.gender
            record_staff.birthday = int(staff.birthday)
            record_staff.status = staff.status

            db.add(record_staff)

            db.commit()

            return format_data_return(response_data={'data': {
                                                        'result': to_dict(record_staff)
                                                    }},
                                      response_http_code=200)

        except Exception as e:
            print(traceback.format_exc())
            return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                      response_http_code=400)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.put(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def update_staff(id, staff: SchemaStaff, db: Session = Depends(get_db)):
    try:
        if string_is_not_valid_uuid(id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": mã nhân viên không đúng định dạng",
                                      response_http_code=400)

        if string_is_null_or_empty(staff.name) or string_is_null_or_empty(staff.code):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên nhân viên hoặc mã nhân viên trống",
                                      response_http_code=400)

        if string_is_null_or_empty(staff.email) and not is_valid_email(staff.email):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": email không đúng định dạng",
                                      response_http_code=400)

        if string_is_not_valid_uuid(staff.position_id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id chức vụ không đúng định dạng",
                                      response_http_code=400)

        if string_is_not_valid_uuid(staff.department_id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id phòng ban không đúng định dạng",
                                      response_http_code=400)

        record_staff = db.query(Staff).filter(
            Staff.id == id).filter(
            Staff.deleted == False).first()

        if not record_staff:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy nhân viên",
                                      response_http_code=404)

        elif record_staff.email != staff.email:
            record_staff_email = db.query(Staff).filter(
                Staff.id != id).filter(
                Staff.email == staff.email).filter(
                Staff.deleted == False).first()

            if record_staff_email:
                return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": email nhân viên đã tồn tại",
                                          response_http_code=400)

        elif record_staff.code != staff.code:
            record_staff_code = db.query(Staff).filter(
                Staff.id != id).filter(
                Staff.code == staff.code).filter(
                Staff.deleted == False).first()

            if record_staff_code:
                return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": mã nhân viên đã tồn tại",
                                          response_http_code=400)
        try:

            if staff.position_id != record_staff.position_id:
                record_position = db.query(Position).filter(
                    Position.id == staff.position_id).filter(
                    Position.deleted == False).first()

                record_staff.position_id = record_position.id
                record_staff.position_name = record_position.name

            if staff.department_id != record_staff.department_id:
                record_department = db.query(Department).filter(
                    Department.id == staff.department_id).filter(
                    Department.deleted == False).first()

                record_staff.department_id = record_department.id
                record_staff.department_name = record_department.name

            record_staff.name = staff.name
            record_staff.code = staff.code
            record_staff.email = staff.email
            record_staff.address = staff.address
            record_staff.phone_number = staff.phone_number
            record_staff.gender = staff.gender
            record_staff.birthday = int(staff.birthday)
            record_staff.status = staff.status

            db.commit()

            return format_data_return(response_data={'data': {
                                                        'result': to_dict(record_staff)
                                                    }},
                                      response_http_code=200)

        except Exception as e:
            print(traceback.format_exc())
            return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                      response_http_code=400)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API, dependencies=[Depends(JWTBearer)])
async def get_staff(request: Request, name: Optional[str] = None, position_id: Optional[str] = None, department_id: Optional[str] = None, db: Session = Depends(get_db),  results_per_page: Optional[int] = 10, page: Optional[int] = 1):
    try:
        jwt = JWTBearer()
        token = await jwt.__call__(request)
        user = decodeJWT(token)
        # print(user['id'])

        if not user:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": tài khoản không tồn tại",
                                      response_http_code=404)

        staff = db.query(Staff).filter(
            Staff.id == user['staff_id']).filter(
            Staff.deleted == False).first()

        search_str_unaccent = "%" + unidecode(name.strip().lower()) + "%" if string_is_not_null_and_not_empty(name) else None

        try:
            record_staff = []
            # print(check_department(staff, db))
            if staff.department_id:
                if check_department(staff, db) == 0:
                    department_id = staff.department_id

                    record_staff = db.query(Staff).filter(
                        Staff.deleted == False).filter(
                        or_(Unaccent(Staff.code).ilike(search_str_unaccent),
                            Unaccent(Staff.name).ilike(search_str_unaccent),
                            Unaccent(Staff.email).ilike(search_str_unaccent),
                            ) if search_str_unaccent is not None else True).filter(
                        Staff.position_id == position_id if position_id is not None else True).filter(
                        Staff.department_id == department_id if department_id is not None else True).order_by(
                        Staff.created_at.desc(), Staff.id.desc()).all()

                elif check_department(staff, db) == 1:
                    record_staff = db.query(Staff).filter(
                        Staff.deleted == False).filter(
                        or_(Unaccent(Staff.code).ilike(search_str_unaccent),
                            Unaccent(Staff.name).ilike(search_str_unaccent),
                            Unaccent(Staff.email).ilike(search_str_unaccent),
                            ) if search_str_unaccent is not None else True).filter(
                        Staff.position_id == position_id if position_id is not None else True).filter(
                        Staff.department_id == department_id if department_id is not None else True).order_by(
                        Staff.created_at.desc(), Staff.id.desc()).all()

                elif check_department(staff, db) == 2:
                    department_id = data_department(staff, db)
                    # print(department_id)
                    record_staff = db.query(Staff).filter(
                        Staff.deleted == False).filter(
                        or_(Unaccent(Staff.code).ilike(search_str_unaccent),
                            Unaccent(Staff.name).ilike(search_str_unaccent),
                            Unaccent(Staff.email).ilike(search_str_unaccent),
                            ) if search_str_unaccent is not None else True).filter(
                        Staff.position_id == position_id if position_id is not None else True).filter(
                        Staff.department_id.in_(department_id)).order_by(
                        Staff.created_at.desc(), Staff.id.desc()).all()

            else:
                record_staff = db.query(Staff).filter(
                    Staff.deleted == False).filter(
                    or_(Unaccent(Staff.code).ilike(search_str_unaccent),
                        Unaccent(Staff.name).ilike(search_str_unaccent),
                        Unaccent(Staff.email).ilike(search_str_unaccent),
                        ) if search_str_unaccent is not None else True).filter(
                    Staff.position_id == position_id if position_id is not None else True).order_by(
                    Staff.created_at.desc(), Staff.id.desc()).all()

            list_data_return = pagination(record_staff, results_per_page, page)

            if not list_data_return:
                return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": limit, offset không đúng",
                                          response_http_code=400)

            return format_data_return(response_data={'data': list_data_return},
                                      response_http_code=200)

        except Exception as e:
            print(traceback.format_exc())
            return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                      response_http_code=400)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def get_staff_id(id, db: Session = Depends(get_db)):
    try:
        if string_is_not_valid_uuid(id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": mã nhân viên không đúng định dạng",
                                      response_http_code=400)

        try:
            record_staff = db.query(Staff).filter(
                Staff.id == id).filter(
                Staff.deleted == False).first()

            if not record_staff:
                return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy nhân viên",
                                          response_http_code=404)

            if record_staff.deleted:
                return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": nhân viên đã bị xóa",
                                          response_http_code=404)

            return format_data_return(response_data={'data': {
                                                        'result': to_dict(record_staff)
                                                    }},
                                      response_http_code=200)

        except Exception as e:
            print(traceback.format_exc())
            return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                      response_http_code=400)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.delete(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def delete_staff(id, db: Session = Depends(get_db)):
    try:
        if string_is_not_valid_uuid(id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": mã nhân viên không đúng định dạng",
                                      response_http_code=400)

        try:
            record_staff = db.query(Staff).filter(
                Staff.id == id).filter(
                Staff.deleted == False).first()

            if not record_staff:
                return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy nhân viên",
                                          response_http_code=404)

            record_staff.deleted = True

            db.commit()

            return format_data_return(response_data={'data': {
                                                        'result': to_dict(record_staff)
                                                    }},
                                      response_http_code=200)

        except Exception as e:
            print(traceback.format_exc())
            return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                      response_http_code=400)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
