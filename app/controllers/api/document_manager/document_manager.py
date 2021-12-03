import traceback

from typing import Optional
from fastapi import Depends
from pydantic import BaseModel
from app.database import get_db
from sqlalchemy.orm import Session
from gatco_restapi.helpers import to_dict

from app.const import DocumentStatus

from app.models.staff import Staff
from app.models.document import Document

from app.controllers.api.document_manager import router

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.check import (
    list_string_is_not_valid_uuid,
    string_is_not_valid_uuid
)

URL_API_ID = "/document/{id}"


class SchemaDocumentManager(BaseModel):
    staff_id: Optional[list]

    class Config:
        orm_mode = True


@router.post(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def create_document_manager(id, document_manager: SchemaDocumentManager, db: Session = Depends(get_db)):
    try:
        if list_string_is_not_valid_uuid(document_manager.staff_id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id nhân viên không đúng định dạng uuid",
                                      response_http_code=400)

        if string_is_not_valid_uuid(id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id văn bản không đúng định dạng uuid",
                                      response_http_code=400)

        records_staff = db.query(Staff).filter(
            Staff.id.in_(document_manager.staff_id)).filter(
            Staff.deleted == False).all()

        if not records_staff:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": nhân viên không tồn tại",
                                      response_http_code=404)

        record_document = db.query(Document).filter(
            Document.id == id).filter(
            Document.deleted == False).first()

        if not record_document:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": document không tồn tại",
                                      response_http_code=404)

        record_document.staff = []

        for data_record in records_staff:
            record_document.staff.append(data_record)

        record_document.status = DocumentStatus.RECEIVE

        db.commit()

        return format_data_return(response_data={'data': {
                                                    'result': to_dict(record_document)
                                                }},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
