import os
import traceback

from fastapi import Depends
from app.controllers.core.utils.data.check import string_is_not_valid_uuid
from app.database import get_db
from sqlalchemy.orm import Session
# from fastapi.responses import FileResponse
from aiofiles import os as async_os
from starlette.responses import FileResponse

from app.models.document import Document

from app.controllers.api.upload import router

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.client import format_data_return

URL_API = "/get-file/{file_name}"


@router.get(URL_API, dependencies=[Depends(JWTBearer)], response_class=FileResponse)
async def get_file(file_name, db: Session = Depends(get_db)):
    try:
        path_server = '/home/backend/uploads'
        path = '/home/dat/Documents/ThangLongUniversity/upload'

        try:
            file_path = path_server + '/' + file_name

            return FileResponse(file_path)

        except Exception as e:
            print(traceback.format_exc())
            return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                      response_http_code=400)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
