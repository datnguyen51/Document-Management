import os
import aiofiles
import traceback


from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, File, UploadFile

from app.controllers.api.upload import router

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.client import format_data_return

URL_API = "/upload-file"


@router.post(URL_API, dependencies=[Depends(JWTBearer)])
async def upload(file: UploadFile = File(...)):
    try:
        path_server = '/home/backend/uploads'
        path = '/home/dat/Documents/ThangLongUniversity/upload'

        if not file:
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": file scan văn bản trống",
                                      response_http_code=400)

        try:
            if not os.path.exists(path_server):
                os.makedirs(path_server)
            async with aiofiles.open(path_server + "/" + file.filename, 'wb+') as f:
                await f.write(file.file.read())
            f.close()

            return format_data_return(response_data={'data': {
                                                        'result': file.filename
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
