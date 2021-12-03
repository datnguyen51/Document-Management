import datetime
import traceback

from typing import Optional
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, Request

from app.const import DocumentStatus

from app.models.staff import Staff
from app.models.document import Document
from app.models.document_type import DocumentType
from app.models.department_document import DepartmentDocument

from app.controllers.api.statistic import router

from app.controllers.core.auth.bearer import JWTBearer
from app.controllers.core.auth.handler import decodeJWT

from app.common.message import ErrorMessage
from app.controllers.core.client import format_data_return
from app.controllers.api.statistic import (
    data_statistic_return,
    default_timestamp_day_end,
    default_timestamp_day_start,
    format_data_return_day_manager
)

URL_API = "/manager"
URL_API_LINE = "/manager-line"


@router.get(URL_API, dependencies=[Depends(JWTBearer)])
async def statistic_manager(request: Request, start: Optional[str] = None, end: Optional[str] = None, year: Optional[str] = None, db: Session = Depends(get_db)):
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

        if year:
            year = int(year)

        if year is None:
            year = 2021

        if start is None and end is None:
            start = default_timestamp_day_start(year, 1)
            end = default_timestamp_day_end(year, 12)
        elif start and end:
            start = int(start)
            end = int(end)

        sum_document = db.query(Document).join(DepartmentDocument).filter(
            DepartmentDocument.department_id == record_staff.department_id).filter(
            Document.created_at >= start if start is not None else True).filter(
            Document.created_at <= end if end is not None else True).filter(
            Document.deleted == False).count()

        sum_document_finish = db.query(DepartmentDocument).join(
            Document).filter(
            Document.status == DocumentStatus.FINISH).filter(
            DepartmentDocument.department_id == record_staff.department_id).filter(
            Document.created_at >= start if start is not None else True).filter(
            Document.created_at <= end if end is not None else True).filter(
            Document.deleted == False).count()

        sum_document_not_finish = db.query(DepartmentDocument).join(
            Document).filter(
            Document.status != DocumentStatus.FINISH).filter(
            DepartmentDocument.department_id == record_staff.department_id).filter(
            Document.created_at >= start if start is not None else True).filter(
            Document.created_at <= end if end is not None else True).filter(
            Document.deleted == False).count()

        time_now = datetime.datetime.now()
        time_expires = int(time_now.timestamp())

        sum_document_expire = db.query(DepartmentDocument).join(
            Document).filter(
            DepartmentDocument.department_id == record_staff.department_id).filter(
            Document.created_at >= start if start is not None else True).filter(
            Document.created_at <= end if end is not None else True).filter(
            Document.end_at <= time_expires).filter(
            Document.status != DocumentStatus.FINISH).filter(
            Document.deleted == False).count()

        records_document_type = db.query(DocumentType).filter(
            DocumentType.deleted == False).all()

        list_record_document_type = []
        for data_record_document_type in records_document_type:
            data = {}
            data['name'] = data_record_document_type.name
            data['value'] = db.query(DepartmentDocument).join(
                Document).filter(
                Document.document_type_id == data_record_document_type.id).filter(
                Document.created_at >= start if start is not None else True).filter(
                Document.created_at <= end if end is not None else True).filter(
                Document.deleted == False).count()

            list_record_document_type.append(data)

        data_return = data_statistic_return(sum_document, sum_document_finish, sum_document_not_finish, sum_document_expire, list_record_document_type)

        return format_data_return(response_data={'data': {
                                                    'result': data_return,
                                                }},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API_LINE, dependencies=[Depends(JWTBearer)])
async def statistic_manager_line(request: Request, start: Optional[str] = None, end: Optional[str] = None, year: Optional[str] = None, db: Session = Depends(get_db)):
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

        if year:
            year = int(year)

        if year is None:
            year = 2021

        list_data_return = []
        if start and end:
            start = int(start)
            end = int(end)

            list_data_return = format_data_return_day_manager(start, end, record_staff, db)

        elif not start or not end:
            for i in range(1, 13):
                # print(i)
                data_document = {}
                data_document_finish = {}
                data_document_not_finish = {}

                start = default_timestamp_day_start(year, i)
                if i != 12:
                    end = default_timestamp_day_end(year, i+1)
                elif i == 12:
                    end = default_timestamp_day_end(year+1, 1)

                sum_document = db.query(Document).join(DepartmentDocument).filter(
                    DepartmentDocument.department_id == record_staff.department_id).filter(
                    Document.created_at >= start if start is not None else True).filter(
                    Document.created_at < end if end is not None else True).filter(
                    Document.deleted == False).count()

                data_document["time"] = 'Tháng ' + str(i)
                data_document["value"] = sum_document
                data_document["category"] = 'Số lượng văn bản'

                list_data_return.append(data_document)

                sum_document_finish = db.query(DepartmentDocument).join(Document).filter(
                    DepartmentDocument.department_id == record_staff.department_id).filter(
                    Document.created_at >= start if start is not None else True).filter(
                    Document.created_at < end if end is not None else True).filter(
                    Document.status == DocumentStatus.FINISH).filter(
                    Document.deleted == False).count()

                data_document_finish["time"] = 'Tháng ' + str(i)
                data_document_finish["value"] = sum_document_finish
                data_document_finish["category"] = 'Số lượng văn bản hoàn thành'

                list_data_return.append(data_document_finish)

                sum_document_not_finish = db.query(DepartmentDocument).join(Document).filter(
                    DepartmentDocument.department_id == record_staff.department_id).filter(
                    Document.created_at >= start if start is not None else True).filter(
                    Document.created_at < end if end is not None else True).filter(
                    Document.status != DocumentStatus.FINISH).filter(
                    Document.deleted == False).count()

                data_document_not_finish["time"] = 'Tháng ' + str(i)
                data_document_not_finish["value"] = sum_document_not_finish
                data_document_not_finish["category"] = 'Số lượng văn bản chưa hoàn thành'

                list_data_return.append(data_document_not_finish)

        return format_data_return(response_data={'data': {
                                                    'result': list_data_return,
                                                }},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
