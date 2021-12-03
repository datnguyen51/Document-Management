import traceback
from typing import Optional

from fastapi import Depends
from pydantic import BaseModel
from app.database import get_db
from sqlalchemy.orm import Session
from gatco_restapi.helpers import to_dict

from app.models.unit import Unit
from app.models.document import Document
from app.models.document_type import DocumentType
from app.models.document_expires import DocumentExpires

from app.controllers.api.document_expires import router

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.utils import pagination
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.convert import convert_day_to_timestamp
from app.controllers.core.utils.data.check import (
    string_is_null_or_empty,
    string_is_not_valid_uuid
)

URL_API = "/expires-management"
URL_API_ID = "/expires-management/{id}"


class SchemaDocumentExpires(BaseModel):
    day: int
    unit_id: str
    document_type_id: str

    class Config:
        orm_mode = True


@router.post(URL_API, dependencies=[Depends(JWTBearer)])
async def create_document_expires(document_expires: SchemaDocumentExpires, db: Session = Depends(get_db)):

    if not document_expires.day:
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": ngày hết hạn xử lý trống",
                                  response_http_code=400)

    if string_is_not_valid_uuid(document_expires.unit_id) or string_is_not_valid_uuid(document_expires.document_type_id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id nơi phát hành hoăc id kiểu văn bản trống",
                                  response_http_code=400)

    record_expires = db.query(DocumentExpires).filter(
        DocumentExpires.unit_id == document_expires.unit_id).filter(
        DocumentExpires.document_type_id == document_expires.document_type_id).filter(
        DocumentExpires.deleted == False).first()

    if record_expires:
        return format_data_return(response_message=ErrorMessage.DATA_IS_EXISTS + ": đã tồn tại",
                                  response_http_code=405)

    try:
        record_unit = db.query(Unit).filter(
            Unit.id == document_expires.unit_id).filter(
            Unit.deleted == False).first()

        if not record_unit:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": cơ sở không tồn tại",
                                      response_http_code=404)

        record_document_type = db.query(DocumentType).filter(
            DocumentType.id == document_expires.document_type_id).filter(
            DocumentType.deleted == False).first()

        if not record_document_type:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": kiểu văn bản không tồn tại",
                                      response_http_code=404)

        record_expires = DocumentExpires()

        record_expires.day = document_expires.day
        record_expires.unit_id = record_unit.id
        record_expires.unit_name = record_unit.name
        record_expires.document_type_id = record_document_type.id
        record_expires.document_type_name = record_document_type.name

        record_unit.document_type.append(record_expires)
        record_document_type.unit.append(record_expires)
        db.add(record_document_type)

        records_document = db.query(Document).filter(
            Document.unit_id == document_expires.unit_id).filter(
            Document.document_type_id == document_expires.document_type_id).filter(
            Document.deleted == False).all()

        if records_document:
            for data_record in records_document:
                data_record.end_at = convert_day_to_timestamp(document_expires.day)

        db.commit()

        return format_data_return(response_data={'data': {
            'result': to_dict(record_expires)
            }},
                                    response_http_code=200)


    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.put(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def update_document_expires(id, document_expires: SchemaDocumentExpires, db: Session = Depends(get_db)):
    try:
        if not document_expires.day:
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": ngày hết hạn xử lý văn bản trống",
                                      response_http_code=400)

        if string_is_not_valid_uuid(document_expires.unit_id) or string_is_not_valid_uuid(document_expires.document_type_id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id nơi phát hành hoăc id kiểu văn bản trống",
                                      response_http_code=400)

        record_expires = db.query(DocumentExpires).filter(
            DocumentExpires.id != id).filter(
            DocumentExpires.unit_id == document_expires.unit_id).filter(
            DocumentExpires.document_type_id == document_expires.document_type_id).filter(
            DocumentExpires.deleted == False).first()

        if record_expires:
            return format_data_return(response_message=ErrorMessage.DATA_IS_EXISTS + ": đã tồn tại",
                                      response_http_code=405)

        try:
            record_expires = db.query(DocumentExpires).filter(
                DocumentExpires.id == id).filter(
                DocumentExpires.deleted == False).first()

            if str(record_expires.unit_id) != document_expires.unit_id:
                record_unit = db.query(Unit).filter(
                    Unit.id == document_expires.unit_id).filter(
                    Unit.deleted == False).first()

                if not record_unit:
                    return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": cơ sở không tồn tại",
                                              response_http_code=404)

                record_expires.unit_id = record_unit.id
                record_expires.unit_name = record_unit.name

                record_unit.document_type.append(record_expires)

            if str(record_expires.document_type_id) != document_expires.document_type_id:
                record_document_type = db.query(DocumentType).filter(
                    DocumentType.id == document_expires.document_type_id).filter(
                    DocumentType.deleted == False).first()

                if not record_document_type:
                    return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": kiểu văn bản không tồn tại",
                                              response_http_code=404)

                record_expires.document_type_id = record_document_type.id
                record_expires.document_type_name = record_document_type.name

                record_document_type.unit.append(record_expires)

            record_expires.day = document_expires.day

            records_document = db.query(Document).filter(
                Document.unit_id == document_expires.unit_id).filter(
                Document.document_type_id == document_expires.document_type_id).filter(
                Document.deleted == False).all()

            if records_document:
                for data_record in records_document:
                    data_record.end_at = convert_day_to_timestamp(document_expires.day)

            db.commit()

            return format_data_return(response_data={'data': {
                'result': to_dict(record_expires)
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
async def get_document_expires(db: Session = Depends(get_db), results_per_page: Optional[int] = 10, page: Optional[int] = 1):
    try:
        records_expires = db.query(DocumentExpires).filter(
            DocumentExpires.deleted == False).all()

        list_data_return = pagination(records_expires, results_per_page, page)

        return format_data_return(response_data={'data': list_data_return},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def get_document_expires_id(id, db: Session = Depends(get_db)):
    if string_is_not_valid_uuid(id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id thiết lập thời hạn xử lý văn bản không hợp lệ",
                                  response_http_code=400)

    try:
        record_expires = db.query(DocumentExpires).filter(
            DocumentExpires.id == id).filter(
            DocumentExpires.deleted == False).first()

        return format_data_return(response_data={'data': {
                                                    'result': to_dict(record_expires),
                                                }},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.delete(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def delete_document_expires(id, db: Session = Depends(get_db)):

    if string_is_not_valid_uuid(id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id chức vụ không hợp lệ",
                                  response_http_code=400)

    try:
        record_expires = db.query(DocumentExpires).filter(
            DocumentExpires.id == id).filter(
            DocumentExpires.deleted == False).first()

        record_expires.deleted = True

        db.commit()

        return format_data_return(response_data={'data': {
            'result': {}
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
