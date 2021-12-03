import traceback

from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, Request

from app.const import DocumentStatus, UserRoleStatus

from app.models.document import Document
from app.models.department import Department

from app.controllers.api.document import router

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.check import (
    check_user,
    string_is_not_valid_uuid,
    string_is_null_or_empty
)
from app.controllers.core.utils.data.convert import format_data

URL_API = "/reject-document/{id}"


class SchemaDocumentReject(BaseModel):
    comment: str

    class Config:
        orm_mode = True


@router.put(URL_API, dependencies=[Depends(JWTBearer)])
async def reject_document(id, document: SchemaDocumentReject, request: Request, db: Session = Depends(get_db)):
    try:
        record_account = await check_user(request, db, ErrorMessage)
        record_department = record_account.staff.department

        if record_account.user_role.slug != UserRoleStatus.ADMIN and record_account.user_role.slug != UserRoleStatus.STAFF_LEAD:
            return format_data_return(response_message=ErrorMessage.PERMISSION_ERROR + ": ngơời dùng không có quyền",
                                      response_http_code=403)

        if string_is_not_valid_uuid(id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id văn bản không đúng định dạng uuid",
                                      response_http_code=400)

        if string_is_null_or_empty(document.comment):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": nội dung từ chối văn bản trống",
                                      response_http_code=400)

        record_document = db.query(Document).filter(
            Document.id == id).filter(
            Document.deleted == False).first()

        if not record_document:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": văn bản không tồn tại",
                                      response_http_code=404)

        if record_department.parent_id == None:
            record_department.document.remove(record_document)

        record_document.status = DocumentStatus.REJECT
        record_document.comment = document.comment
        db.commit()

        return format_data_return(response_data={'data': {
            'result': format_data(record_document)
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
