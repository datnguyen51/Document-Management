import traceback

from fastapi import Depends
from app.database import get_db
from sqlalchemy.orm import Session

from app.models.department import Department

from app.controllers.api.department import router
from app.controllers.api.department import format_department_return

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.client import format_data_return

URL_API = "/department-tree"


@router.get(URL_API, dependencies=[Depends(JWTBearer)])
async def get_department_list(db: Session = Depends(get_db)):
    try:
        records_department = db.query(Department).filter(
            Department.deleted == False).filter(
            Department.parent_id == None).first()

        list_data_return = []
        if records_department:
            list_data_return = format_department_return(records_department)

            num_result = db.query(Department).filter(
                Department.deleted == False).count()

        return format_data_return(response_data={'data': {
                                                    'result': list_data_return,
                                                    'total': num_result
                                                }},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
