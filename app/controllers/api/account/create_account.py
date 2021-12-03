import traceback

from fastapi import Depends
from pydantic import BaseModel
from gatco_restapi.helpers import to_dict
from app.controllers.core.utils.data.check import string_is_not_valid_uuid

from app.models.staff import Staff
from app.models.account import Account
from app.models.user_role import UserRole

from app.common.message import ErrorMessage

from app.controllers.api.account import router
from app.controllers.core.auth.bearer import JWTBearer
from app.controllers.core.utils import generate_password
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.convert import hash_password
from app.controllers.core.utils.mail.send_mail import send_password_mail

from app.database import get_db
from sqlalchemy.orm import Session


class SchemaAccount(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


@router.post("/admin-account")
async def account_role(account: SchemaAccount, db: Session = Depends(get_db)):
    try:
        username = account.username
        password = account.password

        record_staff = Staff()
        record_staff.name = 'Nguyen Van Dat'
        record_staff.code = 'A30091'

        db.add(record_staff)
        db.flush()

        record_account = Account()
        record_account.username = username
        record_account.password = hash_password(password)
        record_account.staff = record_staff

        db.add(record_account)
        db.flush()

        db.commit()

        return format_data_return(response_data={'data': {
            'result': to_dict(record_account)
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


class SchemaCreateAccount(BaseModel):
    role_id: str

    class Config:
        orm_mode = True


@router.post("/create-account/{id}", dependencies=[Depends(JWTBearer)])
async def create_account(id, account: SchemaCreateAccount, db: Session = Depends(get_db)):
    try:
        if string_is_not_valid_uuid(account.role_id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id nhóm quyền không hợp lệ",
                                      response_http_code=400)

        record_staff = db.query(Staff).filter(
            Staff.id == id).filter(
            Staff.deleted == False).first()

        if not record_staff:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy nhân viên",
                                      response_http_code=404)

        record_role = db.query(UserRole).filter(
            UserRole.id == account.role_id).filter(
            UserRole.deleted == False).first()

        if not record_role:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy nhóm quyền",
                                      response_http_code=404)

        password = generate_password(8)

        record_account = Account()
        record_account.username = record_staff.email
        record_account.password = hash_password(password)
        record_account.active = True
        record_account.user_role = record_role
        record_account.staff = record_staff

        db.add(record_account)

        record_staff.have_account = True
        # print(record_staff.email)
        await send_password_mail(record_staff, password)

        db.commit()

        return format_data_return(response_data={'data': {
            'result': to_dict(record_account)
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
