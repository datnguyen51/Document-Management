import traceback

from typing import Optional
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import REAL
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, Request
from gatco_restapi.helpers import to_dict

from app.const import DocumentStatus

from app.models.staff import Staff
from app.models.document import Document
from app.models.staff_document import StaffDocument

from app.controllers.api.document_staff import router

from app.controllers.core.auth.bearer import JWTBearer
from app.controllers.core.auth.handler import decodeJWT

from app.common.message import ErrorMessage
from app.controllers.core.utils import pagination
from app.controllers.core.client import format_data_return

URL_API = "/document"
URL_API_ID = "/document/{id}"


@router.put(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def update_document_staff(id, request: Request, db: Session = Depends(get_db)):
    try:
        jwt = JWTBearer()
        token = await jwt.__call__(request)
        user = decodeJWT(token)
        # print(user['id'])

        if not user:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": tài khoản không tồn tại",
                                      response_http_code=404)

        record_staff = db.query(Staff).filter(
            Staff.id == user['staff_id']).filter(
            Staff.deleted == False).first()

        record_staff_document = db.query(StaffDocument).filter(
            StaffDocument.document_id == id).filter(
            StaffDocument.staff_id == record_staff.id).filter(
            StaffDocument.deleted == False).first()

        if not record_staff_document:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": văn bản không được phân cho nhân viên này",
                                      response_http_code=404)

        record_document = db.query(Document).filter(
            Document.id == id).filter(
            Document.deleted == False).first()

        if not record_document:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": văn bản không tồn tại",
                                      response_http_code=404)

        record_document.status = DocumentStatus.WORKING
        record_staff_document.status = DocumentStatus.WORKING
        db.commit()

        return format_data_return(response_data={'data': {
            'result': to_dict(record_staff_document)
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API, dependencies=[Depends(JWTBearer)])
async def get_document_staff(request: Request, db: Session = Depends(get_db),  results_per_page: Optional[int] = 10, page: Optional[int] = 1):
    try:
        jwt = JWTBearer()
        token = await jwt.__call__(request)
        user = decodeJWT(token)
        # print(user['id'])

        if not user:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": tài khoản không tồn tại",
                                      response_http_code=404)

        record_staff = db.query(Staff).filter(
            Staff.id == user['staff_id']).filter(
            Staff.deleted == False).first()

        records_staff_document = db.query(StaffDocument).filter(
            StaffDocument.staff_id == record_staff.id).filter(
            StaffDocument.deleted == False).all()
        # print(records_department_document)

        list_id_document = []
        for data_record_staff_document in records_staff_document:
            list_id_document.append(
                str(data_record_staff_document.document_id))

        # print(list_id_document)
        records_document = db.query(Document).filter(
            Document.id.in_(list_id_document)).filter(
            Document.deleted == False).all()

        list_data_return = pagination(records_document, results_per_page, page)

        return format_data_return(response_data={'data': list_data_return},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def get_document_staff_id(id, request: Request, db: Session = Depends(get_db)):
    try:
        jwt = JWTBearer()
        token = await jwt.__call__(request)
        user = decodeJWT(token)
        # print(user['id'])

        if not user:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": tài khoản không tồn tại",
                                      response_http_code=404)

        record_staff = db.query(Staff).filter(
            Staff.id == user['staff_id']).filter(
            Staff.deleted == False).first()

        record_document = db.query(Document).filter(
            Document.id == id).filter(
            Document.deleted == False).first()

        record_document_return = to_dict(record_document)

        record_staff_document = db.query(StaffDocument).filter(
            StaffDocument.document_id == id).filter(
            StaffDocument.staff_id == record_staff.id).filter(
            StaffDocument.deleted == False).first()

        record_document_return['request'] = record_staff_document.description if record_staff_document is not None else None

        return format_data_return(response_data={'data': {
            'result': record_document_return
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
