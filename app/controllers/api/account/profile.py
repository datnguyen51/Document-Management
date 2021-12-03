import traceback

from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, Request
from gatco_restapi.helpers import to_dict

from app.models.user_role_permission import UserRolePermission

from app.common.message import ErrorMessage

from app.controllers.api.account import router
from app.controllers.core.auth.bearer import JWTBearer
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.convert import format_data, hash_password
from app.controllers.core.utils.data.check import (
    check_password,
    check_user
)

from app.database import get_db
from sqlalchemy.orm import Session

URL = "/profile"


@router.get(URL, dependencies=[Depends(JWTBearer)])
async def profile(request: Request, db: Session = Depends(get_db)):
    try:
        record_user = await check_user(request, db, ErrorMessage)
        record_staff = record_user.staff

        if not record_staff:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": nhân viên không tồn tại",
                                      response_http_code=404)

        list_permission = []
        if record_user.user_role:
            role = record_user.user_role

            records_role_permission = db.query(UserRolePermission).filter(
                UserRolePermission.user_role_id == role.id).filter(
                UserRolePermission.deleted == False).all()

            for data_permission in records_role_permission:
                list_permission.append(str(data_permission.permission_id))

        try:
            data_user_return = format_data(record_staff)
            data_user_return['permission'] = list_permission

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


class SchemaAccount(BaseModel):
    current_password: Optional[str]
    new_password: Optional[str]
    retype_password: Optional[str]

    class Config:
        orm_mode = True


@router.put(URL + '/change-password', dependencies=[Depends(JWTBearer)])
async def change_password(request: Request, account: SchemaAccount, db: Session = Depends(get_db)):
    try:
        record_account = await check_user(request, db, ErrorMessage)

        if account.new_password != account.retype_password:
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": mật khẩu nhập lại không trùng khớp",
                                      response_http_code=400)

        try:
            if not account.current_password:
                return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": mật khẩu hiện tại trống",
                                          response_http_code=400)
            elif account.current_password and check_password(account.current_password, record_account.password):
                password = hash_password(account.new_password)
                record_account.password = password

                db.commit()

                return format_data_return(response_data={'data': {
                                                            'result': to_dict(record_account)
                                                        }},
                                          response_http_code=200)

            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": mật khẩu hiện tại không khớp",
                                      response_http_code=400)

        except Exception as e:
            print(traceback.format_exc())
            return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                      response_http_code=400)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
