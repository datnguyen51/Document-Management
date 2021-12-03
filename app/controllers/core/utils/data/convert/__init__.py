import time
import bcrypt
import hashlib

from gatco_restapi.helpers import to_dict


def convert_string_list_to_list(strg, separator_mark=","):
    """
    Example:
    :param strg: "A,B,C,D"
    :param separator_mark: ","
    :return: ["A", "B", "C", "D"]
    if exception appear :return None
    """
    try:
        return [sub_str.strip() for sub_str in strg.split(separator_mark)]
    except:
        pass
    return


def convert_list_to_string(lst):
    if not lst:
        return

    string_return = ""
    try:
        for data in lst:
            string_return += str(data) + ","
        return string_return
    except:
        pass
    return


def convert_string_to_long(strg):
    try:
        return int(hashlib.md5(strg.encode("utf-8")).hexdigest()[:6], 16)
    except:
        return 0


def convert_day_to_timestamp(day):
    day_return = day*86400 + time.time()
    return day_return


def hash_password(password):
    password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    return password.decode("utf-8")


def format_data(record_data):
    data_return = to_dict(record_data)

    del data_return['created_by']
    del data_return['updated_at']
    del data_return['updated_by']
    del data_return['deleted']
    del data_return['deleted_at']
    del data_return['deleted_by']

    return data_return


def format_data_account(record_data):
    data_return = to_dict(record_data)

    data_return['role_name'] = record_data.user_role.name if record_data.user_role else None
    data_return['staff_code'] = record_data.staff.code if record_data.staff else None
    data_return['staff_name'] = record_data.staff.name if record_data.staff else None

    del data_return['created_at']
    del data_return['updated_at']
    del data_return['updated_by']
    del data_return['deleted']
    del data_return['deleted_at']
    del data_return['deleted_by']
    del data_return['password']

    return data_return


def format_data_document(record_data, record_user):
    data_return = to_dict(record_data)

    record_staff = record_user.staff
    record_department = record_staff.department

    if not record_data.document_parent_id:
        list_document_children = []
        if record_data.document_children:
            if record_user.user_role.slug == 'staff':
                for data_record in record_data.document_children:
                    if data_record in record_staff.document:
                        data = format_data(data_record)
                        data['file_name'] = convert_string_list_to_list(data_record.file_name)
                        list_document_children.append(data)
            else:
                for data_record in record_data.document_children:
                    if data_record in record_department.document:
                        data = format_data(data_record)
                        data['file_name'] = convert_string_list_to_list(data_record.file_name)
                        list_document_children.append(data)

        del data_return['updated_at']
        del data_return['updated_by']
        del data_return['deleted']
        del data_return['deleted_at']
        del data_return['deleted_by']

        data_return['file_name'] = convert_string_list_to_list(record_data.file_name)

        if list_document_children != []:
            data_return['children'] = list_document_children

        return data_return
