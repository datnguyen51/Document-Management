import traceback

from typing import Optional
from fastapi import Depends, Request
from app.database import get_db
from sqlalchemy.orm import Session
from app.controllers.core.utils.data.check import check_user

from app.controllers.api.document import router

from app.controllers.core.auth.bearer import JWTBearer

from app.common.message import ErrorMessage
from app.controllers.core.client import format_data_return

from app.controllers.api.document import (
    SchemaDocument,
    TypeDocument,
    create_update_document,
    show_document,
    delete
)

URL_API = "/document-internal"
URL_API_ID = "/document-internal/{id}"


@router.post(URL_API, dependencies=[Depends(JWTBearer)])
async def create_document(request: Request, document: SchemaDocument, db: Session = Depends(get_db)):
    try:
        record_account = await check_user(request, db, ErrorMessage)

        data_return = create_update_document(
            document, TypeDocument.DOCUMENT_INTERNAL, db, record_account)

        return data_return

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.put(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def update_document(id, request: Request, document: SchemaDocument, db: Session = Depends(get_db)):
    try:
        record_account = await check_user(request, db, ErrorMessage)

        data_return = create_update_document(
            document, TypeDocument.DOCUMENT_INTERNAL, db, record_account, id)

        return data_return

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API, dependencies=[Depends(JWTBearer)])
async def get_document(request: Request, status: Optional[str] = None, db: Session = Depends(get_db),  results_per_page: Optional[int] = 10, page: Optional[int] = 1):
    try:
        record_account = await check_user(request, db, ErrorMessage)

        data_return = show_document(
            db, record_account, TypeDocument.DOCUMENT_INTERNAL, status, results_per_page, page)
        return data_return

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.get(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def get_document_id(id, request: Request, db: Session = Depends(get_db)):
    try:
        record_account = await check_user(request, db, ErrorMessage)

        data_return = show_document(db, record_account, TypeDocument.DOCUMENT_INTERNAL,
                                    status=None, results_per_page=None, page=None, id=id)
        return data_return

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)


@router.delete(URL_API_ID, dependencies=[Depends(JWTBearer)])
async def delete_document(id, request: Request, db: Session = Depends(get_db)):
    try:
        record_account = await check_user(request, db, ErrorMessage)

        data_return = delete(db, record_account, id)
        return data_return

    except Exception as e:
        print(traceback.format_exc())
        return format_data_return(response_message=ErrorMessage.SYSTEM_ERROR + str(e),
                                  response_http_code=400)
