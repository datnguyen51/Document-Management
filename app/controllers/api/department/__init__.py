from app import URL
from fastapi import APIRouter
from gatco_restapi.helpers import to_dict


router = APIRouter(
    prefix="/department" + URL,
    tags=["department"]
)


def format_department_return(record_department):
    data_return = format_data_json(record_department)
    if record_department.children:
        list_data_children_return = []
        for data_children in record_department.children:
            if data_children.deleted == False:
                data_children_return = format_department_return(data_children)
                list_data_children_return.append(data_children_return)
        data_return['children'] = list_data_children_return
    return data_return


def format_data_json(record_department):
    data_return = to_dict(record_department)

    del data_return["created_at"]
    del data_return["created_by"]
    del data_return["updated_at"]
    del data_return["updated_by"]
    del data_return["deleted"]
    del data_return["deleted_at"]
    del data_return["deleted_by"]
    del data_return["parent_id"]
    del data_return["description"]

    return data_return
