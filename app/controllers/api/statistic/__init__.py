import datetime
from app import URL
from fastapi import APIRouter
from app.database import get_db
from sqlalchemy.orm import Session

from app.const import DocumentStatus
from app.models.document import Document
from app.models.staff_document import StaffDocument
from app.models.department_document import DepartmentDocument


router = APIRouter(
    prefix="/statistic" + URL,
    tags=["statistic"]
)


def data_statistic_return(document, document_finish, document_not_finish, document_expire, list_document_type):
    data_return = {}
    data_document = {}
    data_document['document'] = document
    data_document['finish'] = document_finish
    data_document['not_finish'] = document_not_finish
    data_document['expire'] = document_expire
    data_return['document'] = data_document
    data_return['document_type'] = list_document_type
    return data_return


def check_leap_year(year):
    if (year % 4 == 0) or ((year % 100 == 0 and year % 400 == 0)):
        return True
    return False


def default_timestamp_day_start(year, month):
    day_start = datetime.datetime.timestamp(datetime.datetime(year, month, 1))
    return day_start


def default_timestamp_day_end(year, month):
    day_end = 0
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        day_end = datetime.datetime.timestamp(
            datetime.datetime(year, month, 31))
    elif month == 4 or month == 6 or month == 9 or month == 11:
        day_end = datetime.datetime.timestamp(
            datetime.datetime(year, month, 30))
    elif month == 2:
        if check_leap_year(year):
            day_end = datetime.datetime.timestamp(
                datetime.datetime(year, month, 29))
        else:
            day_end = datetime.datetime.timestamp(
                datetime.datetime(year, month, 28))
    return day_end


def format_data_return_day_admin(start, end, db):
    list_data_return = []
    for i in range(start, end, 86400):
        data_document = {}
        data_document_finish = {}
        data_document_not_finish = {}

        sum_document = db.query(Document).filter(
            Document.created_at >= i).filter(
            Document.created_at <= i + 86400).filter(
            Document.deleted == False).count()
        # print(sum_document)
        # print(start)
        # print(end)
        data_document["time"] = (
            datetime.datetime.fromtimestamp(i)).strftime("%d/%m/%Y")
        data_document["value"] = sum_document
        data_document["category"] = 'Số lượng văn bản'

        list_data_return.append(data_document)

        sum_document_finish = db.query(Document).filter(
            Document.updated_at >= i).filter(
            Document.updated_at <= i + 86400).filter(
            Document.status == DocumentStatus.FINISH).filter(
            Document.deleted == False).count()

        data_document_finish["time"] = (
            datetime.datetime.fromtimestamp(i)).strftime("%d/%m/%Y")
        data_document_finish["value"] = sum_document_finish
        data_document_finish["category"] = 'Số lượng văn bản hoàn thành'

        list_data_return.append(data_document_finish)

        sum_document_not_finish = db.query(Document).filter(
            Document.created_at >= start).filter(
            Document.created_at <= i + 86400).filter(
            Document.status != DocumentStatus.FINISH).filter(
            Document.deleted == False).count()

        data_document_not_finish["time"] = (
            datetime.datetime.fromtimestamp(i)).strftime("%d/%m/%Y")
        data_document_not_finish["value"] = sum_document_not_finish
        data_document_not_finish["category"] = 'Số lượng văn bản chưa hoàn thành'

        list_data_return.append(data_document_not_finish)
    return list_data_return


def format_data_return_day_manager(start, end, record_staff, db):
    list_data_return = []
    for i in range(start, end, 86400):
        data_document = {}
        data_document_finish = {}
        data_document_not_finish = {}

        sum_document = db.query(Document).join(DepartmentDocument).filter(
            DepartmentDocument.department_id == record_staff.department_id).filter(
            Document.created_at >= i).filter(
            Document.created_at <= i + 86400).filter(
            Document.deleted == False).count()
        # print(sum_document)
        # print(start)
        # print(end)
        data_document["time"] = (
            datetime.datetime.fromtimestamp(i)).strftime("%d/%m/%Y")
        data_document["value"] = sum_document
        data_document["category"] = 'Số lượng văn bản'

        list_data_return.append(data_document)

        sum_document_finish = db.query(Document).join(DepartmentDocument).filter(
            DepartmentDocument.department_id == record_staff.department_id).filter(
            Document.updated_at >= i).filter(
            Document.updated_at <= i + 86400).filter(
            Document.status == DocumentStatus.FINISH).filter(
            Document.deleted == False).count()

        data_document_finish["time"] = (
            datetime.datetime.fromtimestamp(i)).strftime("%d/%m/%Y")
        data_document_finish["value"] = sum_document_finish
        data_document_finish["category"] = 'Số lượng văn bản hoàn thành'

        list_data_return.append(data_document_finish)

        sum_document_not_finish = db.query(Document).join(DepartmentDocument).filter(
            DepartmentDocument.department_id == record_staff.department_id).filter(
            Document.created_at >= start).filter(
            Document.created_at <= i + 86400).filter(
            Document.status != DocumentStatus.FINISH).filter(
            Document.deleted == False).count()

        data_document_not_finish["time"] = (
            datetime.datetime.fromtimestamp(i)).strftime("%d/%m/%Y")
        data_document_not_finish["value"] = sum_document_not_finish
        data_document_not_finish["category"] = 'Số lượng văn bản chưa hoàn thành'

        list_data_return.append(data_document_not_finish)
    return list_data_return


def format_data_return_day_staff(start, end, record_staff, db):
    list_data_return = []
    for i in range(start, end, 86400):
        data_document = {}
        data_document_finish = {}
        data_document_not_finish = {}

        sum_document = db.query(Document).join(StaffDocument).filter(
            StaffDocument.staff_id == record_staff.id).filter(
            Document.created_at >= i).filter(
            Document.created_at <= i + 86400).filter(
            Document.deleted == False).count()
        # print(sum_document)
        # print(start)
        # print(end)
        data_document["time"] = (
            datetime.datetime.fromtimestamp(i)).strftime("%d/%m/%Y")
        data_document["value"] = sum_document
        data_document["category"] = 'Số lượng văn bản'

        list_data_return.append(data_document)

        sum_document_finish = db.query(Document).join(StaffDocument).filter(
            StaffDocument.staff_id == record_staff.id).filter(
            Document.updated_at >= i).filter(
            Document.updated_at <= i + 86400).filter(
            Document.status == DocumentStatus.FINISH).filter(
            Document.deleted == False).count()

        data_document_finish["time"] = (
            datetime.datetime.fromtimestamp(i)).strftime("%d/%m/%Y")
        data_document_finish["value"] = sum_document_finish
        data_document_finish["category"] = 'Số lượng văn bản hoàn thành'

        list_data_return.append(data_document_finish)

        sum_document_not_finish = db.query(Document).join(StaffDocument).filter(
            StaffDocument.staff_id == record_staff.id).filter(
            Document.created_at >= start).filter(
            Document.created_at <= i + 86400).filter(
            Document.status != DocumentStatus.FINISH).filter(
            Document.deleted == False).count()

        data_document_not_finish["time"] = (
            datetime.datetime.fromtimestamp(i)).strftime("%d/%m/%Y")
        data_document_not_finish["value"] = sum_document_not_finish
        data_document_not_finish["category"] = 'Số lượng văn bản chưa hoàn thành'

        list_data_return.append(data_document_not_finish)
    return list_data_return
