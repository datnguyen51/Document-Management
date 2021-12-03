import traceback

from typing import Optional
from fastapi import Depends
from pydantic import BaseModel
from app.database import get_db
from sqlalchemy.orm import Session
from gatco_restapi.helpers import to_dict

from app.const import DocumentStatus

from app.models.document import Document
from app.models.department import Department
from app.models.department_document import DepartmentDocument

from app.controllers.api.document_admin import router, SchemaDocument

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.utils import pagination
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.check import (
    list_string_is_not_valid_uuid,
    string_is_not_valid_uuid
)
from app.controllers.core.utils.data.convert import format_data

URL_API = "/document"
URL_API_ID = "/document/{id}"
URL_API_FINISH = "/finish-document/{id}"


class SchemaDocumentAdmin(BaseModel):
    description: Optional[str]
    department_id: Optional[list]
    finish: Optional[bool]
    assignment: Optional[bool]

    class Config:
        orm_mode = True


@router.post(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def document_admin(id, document_admin: SchemaDocumentAdmin, db: Session = Depends(get_db)):
    try:
        if string_is_not_valid_uuid(id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id văn bản không hợp lệ",
                                      response_http_code=400)

        if document_admin.department_id and list_string_is_not_valid_uuid(document_admin.department_id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id phòng ban không hợp lệ",
                                      response_http_code=400)

        record_document = db.query(Document).filter(
            Document.id == id).filter(
            Document.deleted == False).first()

        if not record_document:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": văn bản không tồn tại",
                                      response_http_code=404)

        if document_admin.finish == True:
            if document_admin.department_id:
                records_department = db.query(Department).filter(
                    Department.id.in_(document_admin.department_id)).filter(
                    Department.deleted == False).all()

                if not records_department:
                    return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": phòng ban không tồn tại",
                                              response_http_code=404)

                for record_department in records_department:
                    if record_document not in record_department.document:
                        record_department.document.append(record_document)
                        db.flush()

            if record_document.document_children:
                for data_record in record_document.document_children:
                    data_record.status = DocumentStatus.FINISH
                    db.flush()

            record_document.status = DocumentStatus.FINISH
            db.flush()
        elif document_admin.assignment == True:
            if not document_admin.department_id:
                return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id phòng ban không được trống",
                                          response_http_code=400)

            records_department = db.query(Department).filter(
                Department.id.in_(document_admin.department_id)).filter(
                Department.deleted == False).all()

            if not records_department:
                return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": phòng ban không tồn tại",
                                          response_http_code=404)

            for record_department in records_department:
                if record_document not in record_department.document:
                    record_department.document.append(record_document)
                    db.flush()

            record_document.status = DocumentStatus.PROCESS
        db.commit()
        return format_data_return(response_data={'data': {
            'result': format_data(record_document)
            }},
                                    response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.put(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def update_document_admin(id, document_admin: SchemaDocumentAdmin, db: Session = Depends(get_db)):
    try:
        if document_admin.department_id and string_is_not_valid_uuid(document_admin.department_id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id phòng ban không đúng định dạng uuid",
                                      response_http_code=400)

        try:
            record_department_document = db.query(DepartmentDocument).filter(
                DepartmentDocument.document_id == id).filter(
                DepartmentDocument.deleted == False).first()

            if not record_department_document:
                return format_data_return(response_message=ErrorMessage.DATA_IS_EXISTS + ": văn bản không tồn tại",
                                          response_http_code=404)

            if document_admin.department_id:
                record_department = db.query(Department).filter(
                    Department.id == document_admin.department_id).filter(
                    Department.deleted == False).first()

                if not record_department:
                    return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": phòng ban không tồn tại",
                                              response_http_code=404)

            record_document = db.query(Document).filter(
                Document.id == id).filter(
                Document.deleted == False).first()

            if not record_document:
                return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": document không tồn tại",
                                          response_http_code=404)

            record_department_document.description = document_admin.description
            record_department_document.document_id = record_document.id
            record_department_document.department_id = record_department.id if document_admin.department_id is not None else record_department_document.department_id
            record_department_document.department_name = record_department.name if document_admin.department_id is not None else record_department_document.department_name

            if document_admin.department_id:
                record_department.document.append(record_department_document)

            record_document.department.append(record_department_document)
            record_document.status = DocumentStatus.PROCESS

            db.commit()

            return format_data_return(response_data={'data': {
                'result': to_dict(record_department_document)
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
async def get_document_admin(end: Optional[int] = None, start: Optional[int] = None, status: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        record_department = db.query(Department).filter(
            Department.parent_id == None).filter(
            Department.deleted == False).first()

        # print(record_department.id)
        if not record_department:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": department không tồn tại",
                                      response_http_code=404)

        records_department_document = db.query(DepartmentDocument).filter(
            DepartmentDocument.department_id == record_department.id).filter(
            DepartmentDocument.deleted == False).all()
        # print(records_department_document)

        list_id_document = []
        for data_record_department_document in records_department_document:
            list_id_document.append(str(data_record_department_document.document_id))
        # print(list_id_document)

        list_data_return = []
        num_result = 0
        for data_id in list_id_document:
            record_document = db.query(Document).filter(
                Document.id == data_id).filter(
                Document.created_at <= start if start is not None else True).filter(
                Document.end_at <= end if end is not None else True).filter(
                Document.status == status if status is not None else True).filter(
                Document.deleted == False).first()

            record_document_return = to_dict(record_document)
            # print(record_document_return)
            record_department_document = db.query(DepartmentDocument).filter(
                DepartmentDocument.document_id == data_id).filter(
                DepartmentDocument.department_id != record_department.id).filter(
                DepartmentDocument.deleted == False).first()

            if record_department_document:
                record_document_return['department_work'] = record_department_document.department_name
            else:
                record_document_return['department_work'] = None

            list_data_return.append(record_document_return)
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


@router.get(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def get_document_admin_id(id, db: Session = Depends(get_db)):
    try:
        record_document = db.query(Document).filter(
            Document.id == id).filter(
            Document.deleted == False).first()

        return format_data_return(response_data={'data': {
            'result': to_dict(record_document)
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.put(URL_API_FINISH, dependencies=[Depends(JWTBearer)])
async def process_document(id, document: SchemaDocument, db: Session = Depends(get_db)):
    try:
        if document.department_id:
            if list_string_is_not_valid_uuid(document.document_id):
                return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id của phòng ban không hợp lệ",
                                          response_http_code=400)

        record_document = db.query(Document).filter(
            Document.id == id).filter(
            Document.deleted == False).first()

        if not record_document:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": document không tồn tại",
                                      response_http_code=404)

        if document.department_id:
            records_department = db.query(Department).filter(
                Department.id.in_(document.department_id)).filter(
                Department.deleted == False).all()

            list_department_document = []
            for data_record_department in records_department:
                record_department_document = DepartmentDocument()

                record_department_document.document_id = record_document.id
                record_department_document.department_id = data_record_department.id
                record_department_document.status = DocumentStatus.FINISH

                data_record_department.document.append(record_department_document)
                record_document.department.append(record_department_document)

                list_department_document.append(record_department_document)

            db.add_all(list_department_document)

        else:
            record_department_document = db.query(DepartmentDocument).filter(
                DepartmentDocument.document_id == id).filter(
                DepartmentDocument.deleted == False).first()

            if record_department_document:
                record_department_document.deleted = True
                record_department_document.status = DocumentStatus.FINISH

        record_document.status = DocumentStatus.FINISH

        db.commit()

        return format_data_return(response_data={'data': {
            'result': to_dict(record_department_document)
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
