from functools import wraps
from app.controllers.core.auth.bearer import JWTBearer
from app.controllers.core.auth.handler import decodeJWT
from app.controllers.core.utils.data.check import string_is_not_valid_uuid

from app.models.staff import Staff
from app.models.account import Account
from app.common.message import ErrorMessage
from app.controllers.core.client import format_data_return


def user_verify(f):
    @wraps(f)
    async def decorated(request, db):
        jwt = JWTBearer()
        token = await jwt.__call__(request)
        user = decodeJWT(token)

        if string_is_not_valid_uuid(user['id']):
            return format_data_return(response_message=ErrorMessage.PARAM_ERROR + ": id không đúng định dạng uuid",
                                      response_http_code=400)

        if not user:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": tài khoản không tồn tại",
                                      response_http_code=404)

        record_user = db.query(Account).filter(
            Account.id == user['id']).filter(
            Account.deleted == False).first()

        if not record_user:
            return format_data_return(response_message=ErrorMessage.DATA_NOT_FOUND + ": tài khoản không tồn tại",
                                      response_http_code=404)

    return decorated
