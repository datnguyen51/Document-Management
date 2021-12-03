import traceback

from fastapi import Depends
from pydantic import BaseModel
from gatco_restapi.helpers import to_dict

from app.models.staff import Staff
from app.models.account import Account
from app.models.user_role import UserRole
from app.models.permission import Permission
from app.models.user_role_permission import UserRolePermission

from app.common.message import ErrorMessage

from app.controllers.api.account import router
from app.controllers.core.auth.handler import signJWT
from app.controllers.core.utils import generate_password
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.convert import format_data
from app.controllers.core.utils.data.check import check_password
from app.controllers.core.utils.data.convert import hash_password
from app.controllers.core.utils.mail.send_mail import change_password_mail

from app.database import get_db
from sqlalchemy.orm import Session


class SchemaLogin(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


@router.post("/login")
async def login(account: SchemaLogin, db: Session = Depends(get_db)):
    try:
        record_account = db.query(Account).filter(
            Account.username == account.username).filter(
            Account.deleted == False).first()

        if not record_account:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy người dùng",
                                      response_http_code=404)

        record_staff = db.query(Staff).filter(
            Staff.id == record_account.staff_id).filter(
            Staff.deleted == False).first()

        if not record_staff:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy người dùng",
                                      response_http_code=404)

        if check_password(account.password, record_account.password):
            access_token = signJWT(record_account)

            record_role = record_account.user_role

            user_data = format_data(record_account)
            user_data['role'] = record_role.slug
            user_data['role_name'] = record_role.name

            list_permission = []
            if record_role:
                records_user_permission = db.query(UserRolePermission).filter(
                    UserRolePermission.user_role_id == record_role.id).filter(
                    UserRolePermission.deleted == False).all()

                for data_user_permission in records_user_permission:
                    record_permission = db.query(Permission).filter(
                        Permission.id == data_user_permission.permission_id).filter(
                        Permission.deleted == False).first()
                    list_permission.append(str(record_permission.id))
                user_data['permission'] = list_permission

                del user_data['password']
                del user_data['role_id']

            return format_data_return(response_data={'data': {
                'result': user_data,
                'access_token': access_token}},
                response_http_code=200)

        return format_data_return(response_message=ErrorMessage.PARAM_ERROR,
                                  response_http_code=400)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


class SchemaResetPassword(BaseModel):
    username: str

    class Config:
        orm_mode = True


@router.post("/forgot-password")
async def reset_password(account: SchemaResetPassword, db: Session = Depends(get_db)):
    try:
        record_account = db.query(Account).filter(
            Account.username == account.username).filter(
            Account.deleted == False).first()

        if not record_account:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy người dùng",
                                      response_http_code=404)

        record_staff = db.query(Staff).filter(
            Staff.id == record_account.staff_id).filter(
            Staff.deleted == False).first()

        if not record_staff:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy người dùng",
                                      response_http_code=404)

        password = generate_password(8)

        record_account.password = hash_password(password)
        record_account.staff = record_staff

        await change_password_mail(record_staff, password)

        db.commit()

        user_data = to_dict(record_account)

        return format_data_return(response_data={'data': {
                                                    'result': user_data
                                                }},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
