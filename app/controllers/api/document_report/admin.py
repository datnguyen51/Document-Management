import traceback

from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, Request
from gatco_restapi.helpers import to_dict

from app.const import DocumentStatus, ReportStatus

from app.models.document import Document
from app.models.department import Department
from app.models.work_report import WorkReport
from app.models.staff_document import StaffDocument

from app.controllers.api.document_report import router

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.utils import pagination
from app.controllers.core.client import format_data_return

URL_API = "/admin-report"
URL_API_ID = "/admin-report/{id}"


class SchemaAdminReport(BaseModel):
    reject: Optional[str]
    approve: Optional[str]
    review_description: Optional[str]

    class Config:
        orm_mode = True


@router.put(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def update_admin_report(id, admin_report: SchemaAdminReport, db: Session = Depends(get_db)):
    try:
        record_work_report = db.query(WorkReport).filter(
            WorkReport.id == id).filter(
            WorkReport.deleted == False).first()

        if not record_work_report:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": báo cáo công việc không tồn tại",
                                      response_http_code=404)

        if admin_report.reject:
            record_work_report.review_description = admin_report.review_description
            record_work_report.status = ReportStatus.REJECT

        elif admin_report.approve:
            record_work_report.review_description = admin_report.review_description
            record_work_report.status = ReportStatus.FINISH

            record_staff_document = db.query(StaffDocument).filter(
                StaffDocument.staff_id == record_work_report.staff_id).filter(
                StaffDocument.document_id == record_work_report.document_id).filter(
                StaffDocument.deleted == False).first()

            record_document = db.query(Document).filter(
                Document.id == record_work_report.document_id).filter(
                Document.deleted == False).first()

            if record_document:
                record_document.status = DocumentStatus.FINISH
            if record_staff_document:
                record_staff_document.status = DocumentStatus.FINISH

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
async def get_admin_report(db: Session = Depends(get_db),  results_per_page: Optional[int] = 10, page: Optional[int] = 1):
    try:
        records_work_report = db.query(WorkReport).filter(
            WorkReport.status != ReportStatus.REJECT).filter(
            WorkReport.deleted == False).all()

        list_data_return = pagination(records_work_report, results_per_page, page)

        return format_data_return(response_data={'data': list_data_return},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def get_admin_report_id(id, db: Session = Depends(get_db)):
    try:
        record_department = db.query(Department).filter(
            Department.parent_id == None).filter(
            Department.deleted == False).first()

        if not record_department:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": phòng ban không tồn tại",
                                      response_http_code=404)

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
