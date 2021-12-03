import datetime
import traceback
from typing import Optional

from fastapi import Depends, Request
from app.database import get_db
from sqlalchemy.orm import Session

from app.const import DocumentStatus
from app.models.document import Document

from app.common.message import ErrorMessage
from app.controllers.core.utils import pagination
from app.controllers.core.auth.bearer import JWTBearer
from app.controllers.api.document_expires import router
from app.controllers.core.client import format_data_return
from app.controllers.core.utils.data.check import check_user

URL_API = "/document"


@router.get(URL_API, dependencies=[Depends(JWTBearer)])
async def get_document_expires(request: Request, db: Session = Depends(get_db),  results_per_page: Optional[int] = 10, page: Optional[int] = 1):
    try:
        record_user = await check_user(request, db, ErrorMessage)

        time_now = datetime.datetime.now()
        time_expires = int(time_now.timestamp())

        records_document = db.query(Document).filter(
            Document.end_at <= time_expires).filter(
            Document.status != DocumentStatus.FINISH).filter(
            Document.deleted == False).all()

        if records_document:
            for data_record in records_document:
                data_record.status = DocumentStatus.EXPIRE
                db.flush()
            db.commit()

        list_data_return = pagination(records_document, results_per_page, page,  'document', record_user)

        return format_data_return(response_data={'data': list_data_return},
                                  response_http_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
