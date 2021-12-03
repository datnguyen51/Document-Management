import traceback

from fastapi import Depends
from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from sqlalchemy.orm import Session
from gatco_restapi.helpers import to_dict

from app.models.document_type import DocumentType

from app.controllers.api.document_type import router

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.utils import pagination
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.check import (
    string_is_null_or_empty,
    string_is_not_valid_uuid
)

URL_API = "/document-type-management"
URL_API_ID = "/document-type-management/{id}"


class SchemaDocumentType(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


@router.post(URL_API, dependencies=[Depends(JWTBearer)])
async def create_document_type(document_type: SchemaDocumentType, db: Session = Depends(get_db)):
    if string_is_null_or_empty(document_type.name):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên kiểu văn bản trống",
                                  response_http_code=400)

    record_document_type = db.query(DocumentType).filter(
        DocumentType.name == document_type.name).filter(
        DocumentType.deleted == False).first()

    if record_document_type:
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": kiểu văn bản đã tồn tại",
                                  response_http_code=400)

    try:
        record_document_type = DocumentType()

        record_document_type.name = document_type.name
        record_document_type.description = document_type.description

        db.add(record_document_type)
        db.commit()

        return format_data_return(response_data={'data': {
            'result': to_dict(record_document_type)
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.put(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def update_document_type(id, document_type: SchemaDocumentType, db: Session = Depends(get_db)):

    if string_is_not_valid_uuid(id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id kiểu văn bản không hợp lệ",
                                  response_http_code=400)

    if string_is_null_or_empty(document_type.name):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên kiểu văn bản trống",
                                  response_http_code=400)

    record_document_type = db.query(DocumentType).filter(
        DocumentType.id == id).filter(
        DocumentType.deleted == False).first()

    if not record_document_type:
        return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy kiểu văn bản",
                                  response_http_code=404)

    elif record_document_type.name != document_type.name:
        record_document_type_name = db.query(DocumentType).filter(
            DocumentType.id != id).filter(
            DocumentType.name == document_type.name).filter(
            DocumentType.deleted == False).first()

        if record_document_type_name:
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên kiểu văn bản đã tồn tại",
                                      response_http_code=400)

    try:

        record_document_type.name = document_type.name
        record_document_type.description = document_type.description

        db.commit()

        return format_data_return(response_data={'data': {
            'result': to_dict(record_document_type)
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API, dependencies=[Depends(JWTBearer)])
async def get_document_type(db: Session = Depends(get_db),  results_per_page: Optional[int] = 10, page: Optional[int] = 1):
    try:
        records_document_type = db.query(DocumentType).filter(
            DocumentType.deleted == False).all()

        list_data_return = pagination(records_document_type, results_per_page, page)

        return format_data_return(response_data={'data': list_data_return},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def get_document_type_id(id, db: Session = Depends(get_db)):
    if string_is_not_valid_uuid(id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id kiểu văn bản không hợp lệ",
                                  response_http_code=400)

    try:

        record_document_type = db.query(DocumentType).filter(
            DocumentType.id == id).filter(
            DocumentType.deleted == False).first()

        if not record_document_type:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy đơn vị hợp lệ",
                                      response_http_code=404)

        return format_data_return(response_data={'data': {
            'result': to_dict(record_document_type)
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.delete(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def delete_document_type(id, db: Session = Depends(get_db)):

    if string_is_not_valid_uuid(id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id kiểu văn bản không hợp lệ",
                                  response_http_code=400)

    record_document_type = db.query(DocumentType).filter(
        DocumentType.id == id).filter(
        DocumentType.deleted == False).first()

    try:
        record_document_type.deleted = True

        db.commit()

        return format_data_return(response_data={'data': {}},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
