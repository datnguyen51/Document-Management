import datetime
import traceback

from typing import Optional
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, Request
from gatco_restapi.helpers import to_dict

from app.const import DocumentStatus, UserRoleStatus
from app.models.department_document import DepartmentDocument

from app.models.document import Document
from app.models.document_type import DocumentType

from app.controllers.api.statistic import router

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.check import check_user
from app.models.staff_document import StaffDocument

URL_API = "/document"


@router.get(URL_API, dependencies=[Depends(JWTBearer)])
async def document(request: Request, status: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        record_account = await check_user(request, db, ErrorMessage)

        record_staff = record_account.staff
        record_user_role = record_account.user_role

        if record_user_role.slug == UserRoleStatus.ADMIN or record_user_role.slug == UserRoleStatus.MANAGER:
            if status == 'not_finish':
                records_document = db.query(Document).filter(
                    Document.status != DocumentStatus.FINISH).filter(
                    Document.deleted == False).all()
            else:
                records_document = db.query(Document).filter(
                    Document.status == status if status is not None else True).filter(
                    Document.deleted == False).all()
        elif record_user_role.slug == UserRoleStatus.STAFF_LEAD:
            if status == 'not_finish':
                records_document = db.query(Document).join(DepartmentDocument).filter(
                    Document.status != DocumentStatus.FINISH).filter(
                    DepartmentDocument.department_id == record_staff.department_id).filter(
                    Document.deleted == False).all()
            else:
                records_document = db.query(Document).join(DepartmentDocument).filter(
                    Document.status == status if status is not None else True).filter(
                    DepartmentDocument.department_id == record_staff.department_id).filter(
                    Document.deleted == False).all()
        elif record_user_role.slug == UserRoleStatus.STAFF:
            if status == 'not_finish':
                records_document = db.query(Document).join(StaffDocument).filter(
                    Document.status !=  DocumentStatus.FINISH).filter(
                    StaffDocument.staff_id == record_staff.id).filter(
                    Document.deleted == False).all()
            else:
                records_document = db.query(Document).join(StaffDocument).filter(
                    Document.status == status if status is not None else True).filter(
                    StaffDocument.staff_id == record_staff.id).filter(
                    Document.deleted == False).all()

        data_return = []

        for data_record in records_document:
            data_return.append(to_dict(data_record))

        return format_data_return(response_data={'data': {
            'result': data_return
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
