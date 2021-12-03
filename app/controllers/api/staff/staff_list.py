import traceback

from fastapi import Depends
from app.database import get_db
from sqlalchemy.orm import Session
from gatco_restapi.helpers import to_dict

from app.models.staff import Staff
from app.models.account import Account

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.api.staff import router
from app.controllers.core.client import format_data_return

URL_API = "/staff-list"


@router.get(URL_API, dependencies=[Depends(JWTBearer)])
async def get_staff(db: Session = Depends(get_db)):
    try:

        try:
            records_account = db.query(Account).filter(
                Account.deleted == False).filter(
                Account.staff_id != None).all()

            list_id_staff = []
            for data_account in records_account:
                list_id_staff.append(str(data_account.staff_id))

            records_staff = db.query(Staff).filter(
                Staff.deleted == False).all()
            # print(list_id_staff)
            list_data_return = []
            for data_staff in records_staff:
                if str(data_staff.id) not in list_id_staff:
                    list_data_return.append(to_dict(data_staff))

            return format_data_return(response_data={'data': {
                'result': list_data_return
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
