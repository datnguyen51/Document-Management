from app import URL
from fastapi import APIRouter

from app.database import get_db
from sqlalchemy.orm import Session
from app.models.position import Position
from app.models.department import Department


router = APIRouter(
    prefix="/staff" + URL,
    tags=["staff"]
)


def data_staff(staff):
    list_position_id = []
    list_position_id = staff_position(str(staff.position_id), list_position_id)
    return list_position_id


def staff_position(position_id, list_position_id, db):
    position = db.query(Position).filter(
        Position.id == position_id).filter(
        Position.deleted == False).first()
    if position.children:
        for data_children in position.children:
            list_position_id.append(str(data_children.id))
            return staff_position(str(data_children.id), list_position_id)
    return list_position_id


def check_position(staff, db):
    position = db.query(Position).filter(
        Position.id == staff.position_id).filter(
        Position.deleted == False).first()

    if position.parent_id is None:
        return 1
    return 0


def data_department(staff, db):
    list_department_id = []
    list_department_id.append(str(staff.department_id))
    list_department_id = staff_department(str(staff.department_id), list_department_id, db)
    return list_department_id


def staff_department(department_id, list_department_id, db):
    department = db.query(Department).filter(
        Department.id == department_id).filter(
        Department.deleted == False).first()

    record_data_children = db.query(Department).filter(
        Department.parent_id == department.id).filter(
        Department.deleted == False).all()

    if record_data_children:
        for data_children in record_data_children:
            list_department_id.append(str(data_children.id))
            return staff_department(str(data_children.id), list_department_id, db)
    return list_department_id


def check_department(staff, db):
    department = db.query(Department).filter(
        Department.id == staff.department_id).filter(
        Department.deleted == False).first()

    if department.parent_id is None:
        return 1
    if department.children is None:
        return 0
    return 2
