import traceback

from typing import Optional
from fastapi import Depends
from pydantic import BaseModel
from unidecode import unidecode
from sqlalchemy.sql.elements import or_
from gatco_restapi.helpers import to_dict

from app.models.account import Account
from app.models.user_role import UserRole

from app.common.message import ErrorMessage

from app.controllers.api.account import router
from app.controllers.core.utils import pagination
from app.controllers.core.auth.bearer import JWTBearer
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.database.sqlalchemy_function import Unaccent
from app.controllers.core.utils.data.check import (
    list_string_is_not_valid_uuid,
    string_is_not_null_and_not_empty,
    string_is_not_valid_uuid
)

from app.database import get_db
from sqlalchemy.orm import Session


@router.get("/account-list", dependencies=[Depends(JWTBearer())])
async def account_list(name: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        search_str_unaccent = "%" + unidecode(name.strip().lower()) + "%" if string_is_not_null_and_not_empty(
            name) else None

        try:
            records_account = db.query(Account).filter(
                Account.deleted == False).filter(
                or_(Unaccent(Account.username).ilike(search_str_unaccent))
                    if search_str_unaccent is not None else True).filter(
                Account.role_id == None).order_by(
                Account.created_at.desc(), Account.id.desc()).all()

            list_data_return = []
            num_result = 0
            for data_account in records_account:
                list_data_return.append(to_dict(data_account))
                num_result += 1

            return format_data_return(response_data={'data': {
                'result': list_data_return,
                'total': num_result
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


@router.get("/account-management", dependencies=[Depends(JWTBearer())])
async def show_account(name: Optional[str] = None, code: Optional[str] = None, db: Session = Depends(get_db),  results_per_page: Optional[int] = 10, page: Optional[int] = 1):
    try:
        name_str_unaccent = "%" + unidecode(name.strip().lower()) + "%" if string_is_not_null_and_not_empty(
            name) else None

        code_str_unaccent = "%" + unidecode(code.strip().lower()) + "%" if string_is_not_null_and_not_empty(
            code) else None

        try:
            records_account = db.query(Account).filter(
                Account.deleted == False).filter(
                Unaccent(Account.username).ilike(name_str_unaccent)
                if name_str_unaccent is not None else True,
                Unaccent(Account.staff_code).ilike(code_str_unaccent)
                if code_str_unaccent is not None else True).order_by(
                Account.created_at.desc(), Account.id.desc()).all()

            list_data_return = pagination(records_account, results_per_page, page, 'account')

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


class SchemaAccountRole(BaseModel):
    role_id: str
    account_id: list

    class Config:
        orm_mode = True


@router.put("/account-management", dependencies=[Depends(JWTBearer())])
async def account_role(account_role: SchemaAccountRole, db: Session = Depends(get_db)):
    try:
        account_id = account_role.account_id
        role_id = account_role.role_id

        if list_string_is_not_valid_uuid(account_id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": account_id không đúng định dạng uuid",
                                      response_http_code=400)

        if string_is_not_valid_uuid(role_id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": role_id không đúng định dạng uuid",
                                      response_http_code=400)

        records_account = db.query(Account).filter(
            Account.id.in_(account_id)).filter(
            Account.deleted == False).all()

        if not records_account:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": tài khoản không tồn tại",
                                      response_http_code=404)

        record_user_role = db.query(UserRole).filter(
            UserRole.id == role_id).filter(
            UserRole.deleted == False).first()

        if not record_user_role:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": nhóm người dùng không tồn tại",
                                      response_http_code=404)

        try:
            list_account = []
            for data_account in records_account:
                data_account.role = record_user_role
                data_account.role_name = record_user_role.name

                list_account.append(data_account)

            db.commit()

            return format_data_return(response_data={'data': {
                                                        'result': list_account
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
