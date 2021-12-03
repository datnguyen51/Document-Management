import traceback

from typing import Optional
from fastapi import Depends
from pydantic import BaseModel
from app.database import get_db
from sqlalchemy.orm import Session
from gatco_restapi.helpers import to_dict

from app.models.account import Account
from app.models.user_role import UserRole
from app.models.permission import Permission
from app.models.user_role_permission import UserRolePermission

from app.common.message import ErrorMessage

from app.controllers.api.account import router
from app.controllers.core.auth.bearer import JWTBearer
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.convert import hash_password
from app.controllers.core.utils.data.check import (
    list_string_is_not_valid_uuid,
    string_is_not_valid_uuid,
    string_is_null_or_empty
)

from app.database import get_db
from sqlalchemy.orm import Session


URL_API = "/account-management/{id}"


@router.get(URL_API, dependencies=[Depends(JWTBearer())])
async def account_detail(id, db: Session = Depends(get_db)):
    try:
        if string_is_not_valid_uuid(id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id không đúng định dạng uuid",
                                      response_http_code=400)

        record_user = db.query(Account).filter(
            Account.id == id).filter(
            Account.deleted == False).first()

        if not record_user:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": tài khoản không tồn tại",
                                      response_http_code=404)

        try:
            data_user_return = to_dict(record_user)
            del data_user_return['password']

            return format_data_return(response_data={'data': {
                                                        'result': data_user_return
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


class SchemaAccountUpdate(BaseModel):
    role_id: Optional[str]
    new_password: Optional[str]
    retype_password: Optional[str]

    class Config:
        orm_mode = True


@router.put(URL_API, dependencies=[Depends(JWTBearer())])
async def update_account(id, account: SchemaAccountUpdate, db: Session = Depends(get_db)):
    try:
        if string_is_not_valid_uuid(id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id không đúng định dạng uuid",
                                      response_http_code=400)

        record_user = db.query(Account).filter(
            Account.id == id).filter(
            Account.deleted == False).first()

        if not record_user:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": tài khoản không tồn tại",
                                      response_http_code=404)

        if account.new_password:
            if string_is_null_or_empty(account.retype_password):
                return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": nhập lại mật khẩu không được trống",
                                          response_http_code=400)
            if account.new_password != account.retype_password:
                return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": mật khẩu nhập lại không khớp",
                                          response_http_code=400)

        try:
            if account.new_password:
                password = hash_password(account.new_password)
                record_user.password = password

            if account.role_id:
                record_role = db.query(UserRole).filter(
                    UserRole.id == account.role_id).filter(
                    UserRole.deleted == False).first()

                record_user.role_id = record_role.id
                record_user.role_name = record_role.name

            db.commit()

            return format_data_return(response_data={'data': {
                                                        'result': to_dict(record_user)
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


@router.delete(URL_API, dependencies=[Depends(JWTBearer())])
async def delete_account(id, db: Session = Depends(get_db)):
    try:
        if string_is_not_valid_uuid(id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id không đúng định dạng uuid",
                                      response_http_code=400)

        record_user = db.query(Account).filter(
            Account.id == id).filter(
            Account.deleted == False).first()

        record_user.deleted = True

        db.commit()

        return format_data_return(response_data={'data': {
            'result': []
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
