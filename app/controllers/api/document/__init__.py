import datetime
from typing import Optional

from sqlalchemy.sql.sqltypes import BIGINT, BigInteger

from app import URL
from fastapi import APIRouter
from pydantic.main import BaseModel

from gatco_restapi.helpers import to_dict
from app.const import DocumentStatus, UserRoleStatus

from app.common.message import ErrorMessage
from app.controllers.core.utils import pagination
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.convert import convert_day_to_timestamp, convert_list_to_string, convert_string_list_to_list
from app.controllers.core.utils.data.check import (
    list_is_null_or_empty,
    string_is_null_or_empty,
    string_is_not_valid_uuid
)
from app.models.staff_document import StaffDocument
from app.models.unit import Unit
from app.models.document import Document
from app.models.department import Department
from app.models.document_type import DocumentType
from app.models.department_document import DepartmentDocument

router = APIRouter(
    prefix="/document" + URL,
    tags=["document"]
)


def convert_day_to_timestamp_update(day, created_at):
    day_return = day*86400 + created_at
    return day_return


def convert_data_document_return(records_document, results_per_page, page, record_user=None):
    data_return = {}

    document_init = []
    document_process = []
    document_pending = []
    document_receive = []
    document_working = []
    document_finish = []
    document_reject = []
    num = 0
    for data_document in records_document:
        if data_document.status == DocumentStatus.INITIALIZATION:
            document_init.append(to_dict(data_document))
        elif data_document.status == DocumentStatus.PROCESS:
            document_process.append(to_dict(data_document))
        elif data_document.status == DocumentStatus.PENDING:
            document_pending.append(to_dict(data_document))
        elif data_document.status == DocumentStatus.RECEIVE:
            document_receive.append(to_dict(data_document))
        elif data_document.status == DocumentStatus.WORKING:
            document_working.append(to_dict(data_document))
        elif data_document.status == DocumentStatus.FINISH:
            document_finish.append(to_dict(data_document))
        elif data_document.status == DocumentStatus.REJECT:
            document_reject.append(to_dict(data_document))
        num += 1

    list_data_document = list(document_init + document_process
                              + document_pending + document_receive
                              + document_working + document_finish
                              + document_reject)

    data_return = pagination(list_data_document, results_per_page, page, 'document', record_user)

    return data_return


class SchemaDocument(BaseModel):
    code: Optional[str] = None
    release_code: Optional[str] = None
    name: str
    file_name: list
    description: str
    document_type_id: str
    draft: Optional[str] = None
    signer: Optional[str] = None
    unit_id: Optional[str] = None
    sign_day: Optional[str] = None
    created_at: Optional[str] = None
    document_id: Optional[str] = None
    document_expire: Optional[int] = None
    received_date: Optional[int] = None

    class Config:
        orm_mode = True


class TypeDocument(object):
    DOCUMENT_SENT = 'document-sent'
    DOCUMENT_INCOMING = 'document-incoming'
    DOCUMENT_INTERNAL = 'document-internal'


def create_update_document(document, document_type, db, record_user, id=None):
    if not record_user.user_role:
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": người dùng không thuộc nhóm quyền",
                                  response_http_code=400)

    if string_is_null_or_empty(document.name):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên văn bản trống",
                                  response_http_code=400)

    if document_type != TypeDocument.DOCUMENT_INCOMING:
        if string_is_null_or_empty(document.code):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": mã văn bản trống",
                                      response_http_code=400)

    if string_is_null_or_empty(document.description):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": nội dung văn bản trống",
                                  response_http_code=400)

    if list_is_null_or_empty(document.file_name):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên file scan văn bản trống",
                                  response_http_code=400)

    if record_user.user_role.slug == UserRoleStatus.MANAGER or record_user.user_role.slug == UserRoleStatus.ADMIN:
        if document_type == TypeDocument.DOCUMENT_INCOMING:
            if string_is_null_or_empty(document.signer):
                return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": người ký trống",
                                          response_http_code=400)

            if not document.sign_day:
                return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": ngày ký văn bản trống",
                                          response_http_code=400)

    if document.unit_id and string_is_not_valid_uuid(document.unit_id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id nơi phát hành không đúng định dạng uuid",
                                  response_http_code=400)

    if string_is_not_valid_uuid(document.document_type_id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id kiểu văn bản không đúng định dạng uuid",
                                  response_http_code=400)

    if document.document_id and string_is_not_valid_uuid(document.document_id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id văn bản không đúng định dạng uuid",
                                  response_http_code=400)

    if id:
        if string_is_not_valid_uuid(id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id kiểu văn bản không đúng định dạng uuid",
                                      response_http_code=400)

        record_document = db.query(Document).filter(
            Document.id == id).filter(
            Document.deleted == False).first()

        if not record_document:
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": không tìm thấy văn bản",
                                      response_http_code=400)

        elif record_document.code != document.code:
            record_document_code = db.query(Document).filter(
                Document.id != id).filter(
                Document.code == document.code).filter(
                Document.deleted == False).first()

            if record_document_code:
                return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": mã văn bản đã tồn tại",
                                          response_http_code=400)

        elif record_document.name != document.name:
            record_document_name = db.query(Document).filter(
                Document.id != id).filter(
                Document.name == document.name).filter(
                Document.deleted == False).first()

            if record_document_name:
                return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên bản đã tồn tại",
                                          response_http_code=400)
    else:
        record_document = db.query(Document).filter(
            Document.code == document.code).filter(
            Document.deleted == False).first()

        if record_document:
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": mã văn bản đã tồn tại",
                                      response_http_code=400)

        record_document = db.query(Document).filter(
            Document.name == document.name).filter(
            Document.deleted == False).first()

        if record_document:
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": tên bản đã tồn tại",
                                      response_http_code=400)

    if id:
        if record_document.document_type_id != document.document_type_id:
            record_document_type = db.query(DocumentType).filter(
                DocumentType.id == document.document_type_id).filter(
                DocumentType.deleted == False).first()

            if not record_document_type:
                return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": kiểu văn bản không tồn tại",
                                          response_http_code=404)

            record_document.document_type_id = record_document_type.id if record_document_type is not None else None
            record_document.document_type_name = record_document_type.name if record_document_type is not None else None

        if document.unit_id and record_document.unit_id != document.unit_id:
            record_unit = db.query(Unit).filter(
                Unit.id == document.unit_id).filter(
                Unit.deleted == False).first()

            if not record_unit:
                return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": đơn vị phát hành không tồn tại",
                                          response_http_code=404)

            record_document.unit_id = record_unit.id if record_unit is not None else None
            record_document.unit_name = record_unit.name if record_unit is not None else None

        else:
            record_unit = db.query(Unit).filter(
                Unit.name == record_user.staff.department.name).filter(
                Unit.deleted == False).first()

            if not record_unit:
                record_unit = Unit()
                record_unit.name = record_user.staff.department.name
                db.add(record_unit)
                db.flush()

            record_document.unit_id = record_unit.id if record_unit is not None else None
            record_document.unit_name = record_unit.name if record_unit is not None else None

        if document.release_code:
            record_document.release_code = document.release_code if document.release_code is not None else record_document.release_code

        record_document.name = document.name
        record_document.code = document.code
        record_document.type = document_type
        record_document.signer = document.signer
        record_document.sign_day = document.sign_day
        record_document.file_name = convert_list_to_string(document.file_name)
        record_document.description = document.description
        record_document.created_at = document.created_at if document.created_at is not None else None
        # record_document.status = DocumentStatus.INITIALIZATION

        if record_user.user_role.slug != UserRoleStatus.STAFF:
            if document.document_expire:
                day_expires = document.document_expire

                record_document.end_at = convert_day_to_timestamp(
                    day_expires) if day_expires is not None else None
                record_document.document_expire = document.document_expire
    else:
        record_document_type = db.query(DocumentType).filter(
            DocumentType.id == document.document_type_id).filter(
            DocumentType.deleted == False).first()

        if not record_document_type:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": kiểu văn bản không tồn tại",
                                      response_http_code=404)

        record_document = Document()

        if document.unit_id:
            record_unit = db.query(Unit).filter(
                Unit.id == document.unit_id).filter(
                Unit.deleted == False).first()

            if not record_unit:
                return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": đơn vị phát hành không tồn tại",
                                          response_http_code=404)

        else:
            record_unit = db.query(Unit).filter(
                Unit.name == record_user.staff.department.name).filter(
                Unit.deleted == False).first()

            if not record_unit:
                record_unit = Unit()
                record_unit.name = record_user.staff.department.name
                db.add(record_unit)
                db.flush()

        record_document.unit_id = record_unit.id if record_unit is not None else None
        record_document.unit_name = record_unit.name if record_unit is not None else None

        if document.release_code:
            record_document.release_code = document.release_code

        if document_type == TypeDocument.DOCUMENT_INCOMING:
            document.release_code = document.code

        record_document.name = document.name
        record_document.code = document.code
        record_document.type = document_type
        record_document.file_name = convert_list_to_string(document.file_name)
        record_document.description = document.description
        record_document.created_by = record_user.staff.department.name if record_user.staff.department.name is not None else None
        record_document.document_type_id = record_document_type.id if record_document_type is not None else None
        record_document.document_type_name = record_document_type.name if record_document_type is not None else None
        record_document.created_at = document.created_at if document.created_at is not None else None

        record_document.status = DocumentStatus.INITIALIZATION

        if record_user.user_role.slug != UserRoleStatus.STAFF:
            if document.document_expire:
                day_expires = document.document_expire

                record_document.end_at = convert_day_to_timestamp(
                    day_expires) if day_expires is not None else None
                record_document.document_expire = document.document_expire

        time_now = datetime.datetime.now()
        time_expires = int(time_now.timestamp())

        if record_user.user_role.slug == UserRoleStatus.ADMIN:
            record_document.signer = record_user.staff.name
            record_document.sign_day = time_expires
        else:
            record_document.signer = document.signer
            record_document.sign_day = document.sign_day

        if document.document_id:
            record_document_parent = db.query(Document).filter(
                Document.id == document.document_id).filter(
                Document.deleted == False).first()

            if not record_document_parent:
                return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": văn bản công việc không tồn tại",
                                          response_http_code=404)

            record_document.type = None
            record_document.document_parent_id = record_document_parent.id
            record_document.document_parent_name = record_document_parent.name

        if record_user.user_role.slug == UserRoleStatus.STAFF:
            record_staff = record_user.staff
            record_staff.document.append(record_document)

        record_staff = record_user.staff
        record_department = record_staff.department
        record_document.department.append(record_department)

        db.add(record_document)
    db.commit()
    # print(record_document.staff)
    return format_data_return(response_data={'data': {
        'result': to_dict(record_document)
    }},
        response_http_code=200)


def show_document(db, record_user, document_type=None, status=None, results_per_page=None, page=None, id=None):
    record_staff = record_user.staff
    record_role = record_user.user_role
    if id:
        if string_is_not_valid_uuid(id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id văn bản không hợp lệ",
                                      response_http_code=400)

        record_document = db.query(Document).filter(
            Document.id == id).filter(
            Document.deleted == False).first()

        if not record_document:
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": không tìm thấy văn bản",
                                      response_http_code=400)

        data_return = to_dict(record_document)
        data_return['file_name'] = convert_string_list_to_list(record_document.file_name)

        return format_data_return(response_data={'data': {
            'result': data_return
        }},
            response_http_code=200)
    else:
        list_data_return = []
        # print(record_role.slug)
        if record_role.slug != UserRoleStatus.STAFF:
            records_document = db.query(Document).join(
                DepartmentDocument).filter(
                DepartmentDocument.department_id == record_staff.department_id).filter(
                Document.deleted == False).filter(
                Document.type == document_type).filter(
                Document.status == status if status is not None else True).order_by(
                Document.created_at.asc(), Document.id.desc()).all()

        elif record_role.slug == UserRoleStatus.STAFF:
            records_document = db.query(Document).join(
                StaffDocument).filter(
                StaffDocument.staff_id == record_staff.id).filter(
                Document.deleted == False).filter(
                Document.type == document_type).filter(
                Document.status == status if status is not None else True).order_by(
                Document.created_at.asc(), Document.id.desc()).all()

        if records_document:
            time_now = datetime.datetime.now()
            time_expires = int(time_now.timestamp())

            for data_record in records_document:
                if data_record.end_at and data_record.end_at <= time_expires:
                    data_record.status = DocumentStatus.EXPIRE
                    db.flush()
            db.commit()

        list_data_return = pagination(records_document, results_per_page, page, 'document', record_user)

        return format_data_return(response_data={'data': list_data_return},
                                  response_http_code=200)


def delete(db, record_user, id):
    record_staff = record_user.staff
    if string_is_not_valid_uuid(id):
        return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id văn bản không hợp lệ",
                                  response_http_code=400)

    if record_user.user_role.slug == UserRoleStatus.ADMIN or record_user.user_role.slug == UserRoleStatus.MANAGER:
        record_document = db.query(Document).filter(
            Document.id == id).first()

        if not record_document:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy văn bản",
                                      response_http_code=404)

    elif record_user.user_role.slug == UserRoleStatus.STAFF:
        record_document = db.query(Document).join(
            DepartmentDocument).filter(
            DepartmentDocument.department_id == record_staff.department_id).filter(
            Document.id == id).first()

        if not record_document:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": không tìm thấy văn bản",
                                      response_http_code=404)

    record_document.department = []
    record_document.staff = []

    record_document.deleted = True
    db.commit()
    return format_data_return(response_data={'data': {
        'result': {}
    }},
        response_http_code=200)
