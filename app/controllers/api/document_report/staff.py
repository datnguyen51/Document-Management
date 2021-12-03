import traceback

from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, Request
from gatco_restapi.helpers import to_dict

from app.const import ReportStatus

from app.models.staff import Staff
from app.models.document import Document
from app.models.work_report import WorkReport

from app.controllers.api.document_report import router
from app.controllers.core.auth.handler import decodeJWT

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.utils import pagination
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.check import string_is_not_valid_uuid

URL_API = "/staff-report"
URL_API_ID = "/staff-report/{id}"


class SchemaStaffReport(BaseModel):
    name: Optional[str]
    description: Optional[str]
    document_id: Optional[str]

    class Config:
        orm_mode = True


@router.post(URL_API, dependencies=[Depends(JWTBearer)])
async def create_staff_report(staff_report: SchemaStaffReport, request: Request, db: Session = Depends(get_db)):
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

        if string_is_not_valid_uuid(staff_report.document_id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id văn bản không đúng định dạng uuid",
                                      response_http_code=400)

        try:
            record_document = db.query(Document).filter(
                Document.id == staff_report.document_id).filter(
                Document.deleted == False).first()

            if not record_document:
                return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": văn bản không tồn tại",
                                          response_http_code=404)

            record_work_report = WorkReport()

            record_work_report.name = staff_report.name
            record_work_report.description = staff_report.description
            record_work_report.staff_id = record_staff.id
            record_work_report.staff_name = record_staff.name
            record_work_report.staff_code = record_staff.code
            record_work_report.document_id = record_document.id
            record_work_report.document_name = record_document.name
            record_work_report.department_id = record_staff.department_id
            record_work_report.department_name = record_staff.department_name
            record_work_report.status = ReportStatus.REVIEW

            db.add(record_work_report)
            db.commit()

            return format_data_return(response_data={'data': {
                'result': to_dict(record_work_report)
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


@router.put(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def update_staff_report(id, staff_report: SchemaStaffReport, request: Request, db: Session = Depends(get_db)):
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

        if string_is_not_valid_uuid(staff_report.document_id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id văn bản không đúng định dạng uuid",
                                      response_http_code=400)

        try:
            record_work_report = db.query(WorkReport).filter(
                WorkReport.id == id).filter(
                WorkReport.deleted == False).first()

            if not record_work_report:
                return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": báo cáo công việc không tồn tại",
                                          response_http_code=404)

            record_document = db.query(Document).filter(
                Document.id == staff_report.document_id).filter(
                Document.deleted == False).first()

            if not record_document:
                return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": văn bản không tồn tại",
                                          response_http_code=404)

            record_work_report.name = staff_report.name
            record_work_report.description = staff_report.description
            record_work_report.staff_id = record_staff.id
            record_work_report.staff_name = record_staff.name
            record_work_report.staff_code = record_staff.code
            record_work_report.document_id = record_document.id
            record_work_report.document_name = record_document.name
            record_work_report.department_id = record_staff.department_id
            record_work_report.department_name = record_staff.department_name
            record_work_report.status = ReportStatus.REVIEW

            db.commit()

            return format_data_return(response_data={'data': {
                'result': to_dict(record_work_report)
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
async def get_staff_report(request: Request, status: Optional[str] = None, db: Session = Depends(get_db),  results_per_page: Optional[int] = 10, page: Optional[int] = 1):
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

        records_work_report = db.query(WorkReport).filter(
            WorkReport.staff_id == record_staff.id).filter(
            WorkReport.status == status if status is not None else True).filter(
            WorkReport.deleted == False).all()

        list_data_return = pagination(records_work_report, results_per_page, page)

        return format_data_return(response_data={'data': list_data_return},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def get_staff_report_id(id, db: Session = Depends(get_db)):
    try:
        record_work_report = db.query(WorkReport).filter(
            WorkReport.id == id).filter(
            WorkReport.deleted == False).first()

        if not record_work_report:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": báo cáo công việc không tồn tại",
                                      response_http_code=404)

        return format_data_return(response_data={'data': {
            'result': to_dict(record_work_report),
            }},
                                    response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
