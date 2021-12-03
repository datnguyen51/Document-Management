import traceback

from fastapi import Depends
from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.const import DocumentStatus

from app.models.document import Document
from app.models.department import Department

from app.controllers.api.document import router

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.check import (
    check_user,
    string_is_not_valid_uuid
)
from app.controllers.core.utils.data.convert import format_data

URL_API = "/move-document/{id}"


class SchemaMoveDocument(BaseModel):
    department_id: Optional[list] = None

    class Config:
        orm_mode = True


@router.post(URL_API, dependencies=[Depends(JWTBearer)])
async def move_document(id, request: Request, db: Session = Depends(get_db)):
    try:
        record_account = await check_user(request, db, ErrorMessage)

        if string_is_not_valid_uuid(id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id văn bản không đúng định dạng uuid",
                                      response_http_code=400)

        record_document = db.query(Document).filter(
            Document.id == id).filter(
            Document.deleted == False).first()

        if not record_document:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": văn bản không tồn tại",
                                      response_http_code=404)

        record_department = db.query(Department).filter(
            Department.parent_id == None).filter(
            Department.deleted == False).first()

        if not record_department:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": phòng ban không tồn tại",
                                      response_http_code=404)

        record_department.document.append(record_document)
        record_document.status = DocumentStatus.PENDING

        if record_document.document_parent_id:
            record_document_parent = db.query(Document).filter(
                Document.id == record_document.document_parent_id).filter(
                Document.deleted == False).first()

            if record_document_parent and record_document_parent not in record_department.document:
                record_department.document.append(record_document_parent)

        db.commit()

        return format_data_return(response_data={'data': {
                                                    'result': format_data(record_document)
                                                }},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
