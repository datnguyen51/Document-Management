import traceback
from typing import Optional

from fastapi import Depends
from app.controllers.core.utils.data.check import string_is_not_valid_uuid
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.department import Department

from app.controllers.api.department import router
from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.convert import format_data

URL_API_ID = "/department-list/"


@router.get(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def get_department_list(id: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        if id and string_is_not_valid_uuid(id):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id phòng ban không hợp lệ",
                                      response_http_code=400)

        records_department = db.query(Department).filter(
            Department.id != id if id is not None else True).filter(
            Department.deleted == False).all()

        list_data_return = []
        num_result = 0
        for data_record_department in records_department:
            list_data_return.append(format_data(data_record_department))
            num_result += 1

        return format_data_return(response_data={'data': {
            'result': list_data_return,
            'total': num_result
        }},
            response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
