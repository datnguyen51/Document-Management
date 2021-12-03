import traceback

from fastapi import Depends
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import JSON
from app.database import get_db
from sqlalchemy.orm import Session
from gatco_restapi.helpers import to_dict

from app.models.department import Department

from app.controllers.api.department import router

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.check import (
    string_is_null_or_empty,
    string_is_not_valid_uuid
)

URL_API = "/department-data"


class SchemaDataDepartment(BaseModel):
    department: list

    class Config:
        orm_mode = True


@router.post(URL_API)
async def create_department(department: SchemaDataDepartment, db: Session = Depends(get_db)):
    for data_department in department.department:
        if string_is_null_or_empty(data_department['name']):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên trống",
                                      response_http_code=400)

        if not data_department['created_at']:
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": ngày tạo trống",
                                      response_http_code=400)

        if data_department['children']:
            for data_children in data_department['children']:
                if string_is_null_or_empty(data_department['name']):
                    return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên trống",
                                              response_http_code=400)

                if not data_department['created_at']:
                    return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": ngày tạo trống",
                                              response_http_code=400)

    try:
        list_data_department = []
        for data_department in department.department:
            record_department = db.query(Department).filter(
                Department.name == data_department['name']).filter(
                Department.deleted == False).first()

            if record_department:
                continue

            record_department = Department()

            record_department.name = data_department['name']
            record_department.created_at = data_department['created_at']
            record_department.description = data_department['description']

            db.add(record_department)
            db.flush()

            data_department_json = to_dict(record_department)
            data_department_json['children'] = []
            if data_department['children']:

                for data_children in data_department['children']:

                    record_department_children = db.query(Department).filter(
                        Department.name == data_children['name']).filter(
                        Department.deleted == False).first()

                    if record_department_children:
                        continue

                    record_department_children = Department()

                    record_department_children.name = data_children['name']
                    record_department_children.created_at = data_children['created_at']
                    record_department_children.description = data_children['description']
                    record_department_children.parent_id = record_department.id

                    db.add(record_department_children)
                    db.flush()

                    data_department_json['children'].append(to_dict(record_department_children))

            list_data_department.append(data_department_json)

        db.commit()

        return format_data_return(response_data={'data': {
            'result': list_data_department
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
