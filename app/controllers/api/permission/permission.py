import traceback

from fastapi import Depends
from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from sqlalchemy.orm import Session
from gatco_restapi.helpers import to_dict

from app.models.permission import Permission

from app.controllers.api.permission import router

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.utils import pagination
from app.controllers.core.utils.data.convert import format_data
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.check import (
    string_is_null_or_empty,
    string_is_not_valid_uuid
)

URL_API = "/permission-management"
URL_API_PERMISSION = "/permission-list"


class SchemaPermission(BaseModel):
    permission: list

    class Config:
        orm_mode = True


@router.post(URL_API, dependencies=[Depends(JWTBearer)])
async def create_permission(permission: SchemaPermission, db: Session = Depends(get_db)):
    if not (permission.permission):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": quyền trống",
                                  response_http_code=400)

    list_data_permission = []
    try:
        for data_permission in permission.permission:
            if string_is_null_or_empty(data_permission['type']):
                return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": loại quyền trống",
                                          response_http_code=400)

            if not (data_permission['permission']):
                return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": quyền trống",
                                          response_http_code=400)

            for data_permission_method in data_permission['permission']:
                if string_is_null_or_empty(data_permission_method['name']) or string_is_null_or_empty(data_permission_method['method']):
                    return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên quyền hoặc kiểu quyền trống",
                                              response_http_code=400)

                record_permission = db.query(Permission).filter(
                    Permission.name == data_permission_method['name']).filter(
                    Permission.deleted == False).first()

                if not record_permission:
                    record_permission = Permission()

                    record_permission.name = data_permission_method['name']
                    record_permission.method = data_permission_method['method']
                    record_permission.type = data_permission['type']

                    list_data_permission.append(record_permission)

        db.add_all(list_data_permission)
        db.commit()

        return format_data_return(response_data={'data': {
                                                    'result': list_data_permission
                                                }},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API, dependencies=[Depends(JWTBearer)])
async def get_permission(db: Session = Depends(get_db)):
    try:
        records_permission = db.query(Permission).filter(
            Permission.deleted == False).all()

        list_data_return = []
        for data_permission in records_permission:
            list_data_return.append(to_dict(data_permission))

        return format_data_return(response_data={'data': list_data_return},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API_PERMISSION, dependencies=[Depends(JWTBearer)])
async def delete_permission(db: Session = Depends(get_db)):

    records_permission = db.query(Permission).filter(
        Permission.deleted == False).all()

    if not records_permission:
        return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không có danh sách quyền",
                                  response_http_code=404)

    try:
        list_type_permission = []
        data_permission_return = {}
        for data_record_permission in records_permission:
            if data_record_permission.type not in list_type_permission:
                list_type_permission.append(data_record_permission.type)
                data_permission_return[data_record_permission.type] = {}

        flag_type_permission = ''
        for data_permission in records_permission:
            if data_permission.type != flag_type_permission:
                flag_type_permission = data_permission.type
                data_permission_json = {}

                data_permission_json['Create'] = None
                data_permission_json['Main'] = None
                data_permission_json['Edit'] = None
                data_permission_json['Delete'] = None

            if data_permission.method == 'POST':
                data_permission_json['Create'] = data_permission.id
            elif data_permission.method == 'GET':
                data_permission_json['Main'] = data_permission.id
            elif data_permission.method == 'PUT':
                data_permission_json['Edit'] = data_permission.id
            elif data_permission.method == 'DELETE':
                data_permission_json['Delete'] = data_permission.id

            data_permission_return[data_permission.type] = data_permission_json

        return format_data_return(response_data={'data': {
            "result": data_permission_return
        }},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
