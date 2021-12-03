import bcrypt
import re
from uuid import UUID
from app.controllers.core.auth.bearer import JWTBearer
from app.controllers.core.auth.handler import decodeJWT

from app.controllers.core.client import format_data_return
from app.models.account import Account
from app.models.staff import Staff


def string_is_null_or_empty(str):
    """
    Example 1:
    :param str: "" or "  " or None
    :return: True
    ---------
    Example 2:
    :param str: "  A  " or "B"
    :return: False
    """
    try:
        if str and str.strip():
            return False
    except:
        pass
    return True


def string_is_not_null_and_not_empty(str):
    """
    Example 1:
    :param str: "" or "  " or None
    :return: False
    ---------
    Example 2:
    :param str: "  A  " or "B"
    :return: True
    """
    try:
        if str and str.strip():
            return True
    except:
        pass
    return False


def list_is_null_or_empty(lst):
    """
    Example 1:
    :param lst: [1, 2, 3] or ["A", "B", "C"]
    :return: False
    ---------
    Example 2:
    :param lst: [] or None
    :return: True
    """
    try:
        if lst and len(lst) > 0:
            return False
    except:
        pass
    return True


def list_is_not_null_and_not_empty(lst):
    """
    Example 1:
    :param lst: [1, 2, 3] or ["A", "B", "C"]
    :return: True
    ---------
    Example 2:
    :param lst: [] or None
    :return: False
    """
    try:
        if lst and len(lst) > 0:
            return True
    except:
        pass
    return False


def string_is_not_valid_uuid(uid, version=4):
    """
    Example 1:
    :param uid: "483deb8f-9184-4b10-bd5e-e02df70c2905"
    :param version: 4
    :return: False
    ---------
    Example 2:
    :param uid: "A"
    :param version: 4
    :return: True
    """
    try:
        if UUID(uid).version == version:
            return False
    except:
        pass
    return True


def string_is_valid_uuid(uid, version=4):
    """
    Example 1:
    :param uid: "483deb8f-9184-4b10-bd5e-e02df70c2905"
    :param version: 4
    :return: True
    ---------
    Example 2:
    :param uid: "A"
    :param version: 4
    :return: False
    """
    try:
        if UUID(uid).version == version:
            return True
    except:
        pass
    return False


def list_string_is_valid_uuid(list_string, version=4):
    """
    Example 1:
    :param list_string: ["55f20aec-cc39-4a96-a1dd-f6684c51292a", "483deb8f-9184-4b10-bd5e-e02df70c2905"]
    :param version: 4
    :return: True
    ---------
    Example 2:
    :param list_string: ["55f20aec-cc39-4a96-a1dd-f6684c51292a", "A"]
    :param version: 4
    :return: False
    """
    try:
        for str in list_string:
            if UUID(str).version != version:
                return False
    except:
        return False
    return True


def list_string_is_not_valid_uuid(list_string, version=4):
    """
    Example 1:
    :param list_string: ["55f20aec-cc39-4a96-a1dd-f6684c51292a", "483deb8f-9184-4b10-bd5e-e02df70c2905"]
    :param version: 4
    :return: False
    ---------
    Example 2:
    :param list_string: ["55f20aec-cc39-4a96-a1dd-f6684c51292a", "A"]
    :param version: 4
    :return: True
    """
    try:
        for str in list_string:
            if UUID(str).version != version:
                return True
    except:
        return True
    return False


def is_valid_email(email):
    try:
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
    except:
        pass
    return False


def check_password(current_passw, user_passw):
    current_password = current_passw.encode('utf-8')
    user_password = user_passw.encode('utf-8')
    if bcrypt.checkpw(current_password, user_password):
        return True
    return False


async def check_user(request, db, ErrorMessage):
    jwt = JWTBearer()
    token = await jwt.__call__(request)
    user = decodeJWT(token)

    record_user = db.query(Account).filter(
        Account.id == user['id']).filter(
        Account.deleted == False).first()

    return record_user
