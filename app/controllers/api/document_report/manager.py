import traceback

from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, Request
from gatco_restapi.helpers import to_dict

from app.const import ReportStatus

from app.models.staff import Staff
from app.models.work_report import WorkReport

from app.controllers.api.document_report import router

from app.controllers.core.auth.bearer import JWTBearer
from app.controllers.core.auth.handler import decodeJWT

from app.common.message import ErrorMessage
from app.controllers.core.utils import pagination
from app.controllers.core.client import format_data_return

URL_API = "/manager-report"
URL_API_ID = "/manager-report/{id}"


class SchemaManagerReport(BaseModel):
    reject: Optional[str]
    approve: Optional[str]
    review_description: Optional[str]

    class Config:
        orm_mode = True


@router.put(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def update_manager_report(id, manager_report: SchemaManagerReport, request: Request, db: Session = Depends(get_db)):
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

        record_work_report = db.query(WorkReport).filter(
            WorkReport.id == id).filter(
            WorkReport.department_id == record_staff.department_id).filter(
            WorkReport.deleted == False).first()

        if not record_work_report:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": báo cáo công việc không tồn tại",
                                      response_http_code=404)

        if manager_report.reject:
            record_work_report.review_description = manager_report.review_description
            record_work_report.status = ReportStatus.REJECT

        elif manager_report.approve:
            record_work_report.review_description = manager_report.review_description
            record_work_report.status = ReportStatus.APPROVE

        db.commit()

        return format_data_return(response_data={'data': {
            'result': to_dict(record_work_report)
            }},
                                    response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API, dependencies=[Depends(JWTBearer)])
async def get_manager_report(request: Request, status: Optional[str] = None, db: Session = Depends(get_db),  results_per_page: Optional[int] = 10, page: Optional[int] = 1):
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
            WorkReport.department_id == record_staff.department_id).filter(
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
async def get_manager_report_id(id, request: Request, db: Session = Depends(get_db)):
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

        record_work_report = db.query(WorkReport).filter(
            WorkReport.id == id).filter(
            WorkReport.department_id == record_staff.department_id).filter(
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
