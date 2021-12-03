import math
from app import URL
from fastapi import APIRouter

from gatco_restapi.helpers import to_dict
from app.models.user_role_permission import UserRolePermission


router = APIRouter(
    prefix="/role" + URL,
    tags=["role"]
)


def format_data_role_return(record_role, db):
    list_id_permission = []
    records_role_permission = db.query(UserRolePermission).filter(
        UserRolePermission.user_role_id == record_role.id).filter(
        UserRolePermission.deleted == False).all()

    for data_permission in records_role_permission:
        list_id_permission.append(str(data_permission.permission_id))

    data_return = to_dict(record_role)
    data_return['permission'] = list_id_permission

    return data_return


def format_data_list_role(db, instances=None, results_per_page=10, page=1):
    if type(instances) == dict:
        data = instances
        page_num = 1
        total_pages = 1
        num_results = 1
    else:
        num_results = len(instances)
        try:
            results_per_page = int(results_per_page)
        except:
            return 0
        try:
            page_num = int(page)
        except:
            return 0
        if (results_per_page is None or results_per_page <= 0) or (page_num is None or page_num <= 0):
            results_per_page = 10
            page_num = 1
            start = 0
            end = num_results
            total_pages = 1
        else:
            start = (page_num - 1) * results_per_page
            end = min(num_results, start + results_per_page)
            total_pages = int(math.ceil(num_results / results_per_page))

        list_data_return = []
        for data_record in instances[start:end]:
            data_return = to_dict(data_record)

            list_data_permission = []
            records_role_permission = db.query(UserRolePermission).filter(
                UserRolePermission.user_role_id == data_record.id).filter(
                UserRolePermission.deleted == False).all()

            for data_permission in records_role_permission:
                list_data_permission.append(str(data_permission.permission_id))

            data_return['permission_id'] = list_data_permission
            list_data_return.append(data_return)

        data = list_data_return

    return dict(result=data, page=page_num, total_pages=total_pages, num_results=num_results)
