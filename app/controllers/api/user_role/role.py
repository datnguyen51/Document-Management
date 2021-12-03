import traceback

from fastapi import Depends
from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from sqlalchemy.orm import Session
from gatco_restapi.helpers import to_dict

from app.models.account import Account
from app.models.user_role import UserRole
from app.models.permission import Permission
from app.models.user_role_permission import UserRolePermission

from app.controllers.api.user_role import format_data_list_role, router

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.utils import pagination
from app.controllers.core.utils.data.convert import format_data
from app.controllers.api.user_role import format_data_list_role
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.check import (
    list_string_is_not_valid_uuid,
    string_is_null_or_empty,
    string_is_not_valid_uuid
)

URL_API = "/role-management"
URL_API_ID = "/role-management/{id}"


class SchemaUserRolePermission(BaseModel):
    name: str
    description: Optional[str]
    account_id: Optional[list]
    permission_id: list

    class Config:
        orm_mode = True


@router.post(URL_API, dependencies=[Depends(JWTBearer)])
async def create_role(user_role: SchemaUserRolePermission, db: Session = Depends(get_db)):
    if string_is_null_or_empty(user_role.name):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên quyền trống",
                                  response_http_code=400)

    if user_role.account_id and list_string_is_not_valid_uuid(user_role.account_id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": danh sách tài khoản không hợp lệ",
                                  response_http_code=400)

    if list_string_is_not_valid_uuid(user_role.permission_id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": danh sách các quyền không hợp lệ",
                                  response_http_code=400)

    record_role = db.query(UserRole).filter(
        UserRole.name == user_role.name).filter(
        UserRole.deleted == False).first()

    if record_role:
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": quyền đã tồn tại",
                                  response_http_code=400)

    try:
        record_role = UserRole()

        record_role.name = user_role.name
        record_role.description = user_role.description
        record_role.slug = 'staff'

        db.add(record_role)
        db.flush()

        if user_role.account_id:
            records_account = db.query(Account).filter(
                Account.id.in_(user_role.account_id)).filter(
                Account.deleted == False).all()

            for data_account in records_account:
                data_account.role_id = record_role.id
                data_account.role_name = record_role.name

        records_permission = db.query(Permission).filter(
            Permission.id.in_(user_role.permission_id)).filter(
            Permission.deleted == False).all()

        for data_permission in records_permission:
            record_role.permission.append(data_permission)

            db.flush()
        db.commit()

        return format_data_return(response_data={'data': {
                                                    'result': to_dict(record_role)
                                                }},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API, dependencies=[Depends(JWTBearer)])
async def get_role(db: Session = Depends(get_db), results_per_page: Optional[int] = 10, page: Optional[int] = 1):
    try:
        records_role = db.query(UserRole).filter(
            UserRole.deleted == False).all()

        list_data_return = format_data_list_role(
            db, records_role, results_per_page, page)

        return format_data_return(response_data={'data': list_data_return},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.put(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def update_role(id, user_role: SchemaUserRolePermission, db: Session = Depends(get_db)):
    if string_is_not_valid_uuid(id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id quyền không hợp lệ",
                                  response_http_code=400)

    if string_is_null_or_empty(user_role.name):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên quyền trống",
                                  response_http_code=400)

    if user_role.account_id and list_string_is_not_valid_uuid(user_role.account_id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": danh sách tài khoản không hợp lệ",
                                  response_http_code=400)

    if list_string_is_not_valid_uuid(user_role.permission_id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": danh sách các quyền không hợp lệ",
                                  response_http_code=400)

    record_role = db.query(UserRole).filter(
        UserRole.name == user_role.name).filter(
        UserRole.deleted == False).first()

    if record_role and str(record_role.id) != str(id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": quyền đã tồn tại",
                                  response_http_code=400)

    try:
        record_role = db.query(UserRole).filter(
            UserRole.id == id).filter(
            UserRole.deleted == False).first()

        if record_role.name != user_role.name:
            record_role.name = user_role.name

        record_role.description = user_role.description

        if user_role.account_id:
            records_account = db.query(Account).filter(
                Account.id.in_(user_role.account_id)).filter(
                Account.deleted == False).all()

            for data_account in records_account:
                data_account.role_id = record_role.id
                data_account.role_name = record_role.name

        record_role.permission = []

        records_permission = db.query(Permission).filter(
            Permission.id.in_(user_role.permission_id)).filter(
            Permission.deleted == False).all()

        for data_permission in records_permission:
            record_role.permission.append(data_permission)

            db.flush()
        db.commit()

        return format_data_return(response_data={'data': {
            'result': to_dict(record_role)
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def get_role_detail(id, db: Session = Depends(get_db)):
    try:
        record_role = db.query(UserRole).filter(
            UserRole.id == id).filter(
            UserRole.deleted == False).first()

        if not record_role:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy nhóm người dùng",
                                      response_http_code=404)

        records_permission = db.query(Permission).join(
            Permission.user_role).filter(
            UserRolePermission.user_role_id == id).filter(
            UserRolePermission.deleted == False).all()

        list_data_permission = []
        for data_permission in records_permission:
            data_return = {}
            data_return['id'] = data_permission.id
            data_return['name'] = data_permission.name
            list_data_permission.append(data_return)

        data_user_role = to_dict(record_role)
        data_user_role['permission'] = list_data_permission
        print(len(list_data_permission))

        return format_data_return(response_data={'data': {
            'result': data_user_role
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.delete(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def delete_role(id, db: Session = Depends(get_db)):
    try:
        record_role = db.query(UserRole).filter(
            UserRole.id == id).filter(
            UserRole.deleted == False).first()

        record_role.deleted = True
        db.commit()

        return format_data_return(response_data={'data': {
            'result': {}
        }},
            response_http_code=204)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
