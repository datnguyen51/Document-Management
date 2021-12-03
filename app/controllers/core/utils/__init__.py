import re
import math
import time
import hashlib
import string
import random

from uuid import UUID
from sqlalchemy import *
from hashids import Hashids
from datetime import datetime

from app.controllers.core.utils.data.convert import (
    format_data,
    format_data_account,
    format_data_document
)


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_to_test


def hash_md5(str_input):
    if str_input is not None:
        return hashlib.md5(str_input.encode('utf-8')).hexdigest()
    return None


def is_valid_email(email):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if email_regex.match(email):
        return True
    return False


def get_format_date_time(apply_for, use_for):
    if apply_for is not None and use_for is not None:
        list_format_date_time = {
            "POS_CLIENT": {
                "SALE": "%Y-%m-%d %H:%M:%S",
                "SHIFT": "%Y-%m-%d %H:%M:%S",
                "REPORT": "%Y-%m-%d"
            },
            "POS_CMS": {
                "SHIFT": "%Y-%m-%d %H:%M:%S",
                "REPORT": "%Y-%m-%d",
                "REPORT_OTHER": "%Y-%m-%d",
                "REPORT_BY_HOUR": "%H",
                "SHIFT_LIST": "%Y-%m-%d %H:%M:%S.%f",
                "POS_DEVICE": "%Y-%m-%d %H:%M:%S.%f",
                "SALE": "%Y-%m-%d %H:%M:%S.%f"
            },
            "POS_CMS_AND_CLIENT": {
                "REPORT": "%Y-%m-%d"
            },
            "MASTER_DATA": {
                "SALE": "%Y-%m-%d"
            },
            "DATA_WAREHOUSE": {
                "SALE_IN": "%Y-%m-%d",
                "SALE_OUT": "%Y-%m-%d %H:%M:%S"
            },
            "FOOD_BOOK": {
                "SALE": "%Y-%m-%d %H:%M:%S.%f"
            },
            "ACCOUNTING": {
                "REPORT_PAYMENT_INPUT": "%Y-%m-%d %H:%M:%S",
                "REPORT_PAYMENT_OUTPUT": "%m/%d/%Y",
                "SALE_DETAIL_INPUT": "%Y-%m-%d %H:%M:%S",
                "SALE_DETAIL_OUTPUT": "%m/%d/%Y %I:%M:%S %p",
                "SALE_DETAIL_ONE_RECORD_INPUT": "%Y-%m-%d %H:%M:%S",
                "SALE_DETAIL_ONE_RECORD_INPUT_2": "%Y-%m-%d %H:%M:%S",
                "SALE_DETAIL_ONE_RECORD_INPUT_3": "%Y-%m-%d",
                "SALE_DETAIL_ONE_RECORD_OUTPUT": "%m/%d/%Y"
            },
            "REPORT_ADV": {
                "REVENUE_BY_STORE": "%Y-%m-%d %H:%M:%S",
                "REVENUE_BY_STORE_BY_DAY_INPUT": "%Y-%m-%d %H:%M:%S",
                "REVENUE_BY_STORE_BY_DAY_OUTPUT": "%Y-%m-%d",
                "ITEM_SALES_BY_BRAND": "%d/%m/%Y"
            },
            "REPORT_FABI": {
                "SALE": "%Y-%m-%d %H:%M:%S"
            },
            "PARTNER": {
                "CONNECTION_REQUEST": "%Y-%m-%d %H:%M:%S"
            }
        }
        return (list_format_date_time[apply_for])[use_for] if (list_format_date_time[apply_for])[use_for] is not None else None

    return None


def convert_date_time_to_timestamp(date_time, apply_for, use_for, timestamp_out_type="milliseconds"):
    format_date_time = get_format_date_time(apply_for, use_for)
    date_time = str(date_time)

    if format_date_time is not None:
        try:
            datetime.strptime(date_time, format_date_time)

        except:
            print("\n--- Format Date Time Incorrect")
            return 0

        try:
            if timestamp_out_type == "milliseconds":
                return int(time.mktime(datetime.strptime(date_time, format_date_time).timetuple())) * 1000
            elif timestamp_out_type == "seconds":
                return int(time.mktime(datetime.strptime(date_time, format_date_time).timetuple()))

        except Exception as e:
            print("\n--- Exception when convert Date Time to Timestamp: " + str(e))
            return 0

    return 0


def convert_timestamp_to_date_time(timestamp, apply_for, use_for):
    format_date_time = get_format_date_time(apply_for, use_for)

    if format_date_time is not None:
        timestamp = int(timestamp) / 1000

        try:
            # Local time
            return str(datetime.fromtimestamp(timestamp).strftime(format_date_time))
            # return str(datetime.utcfromtimestamp(timestamp).strftime(format_date_time)) # UTC

        except Exception as e:
            print("\n--- Exception when convert Timestamp to Date Time: " + str(e))
            return None

    return None


def get_day_of_week_by_date_time(date_time, apply_for, use_for):
    format_date_time = get_format_date_time(apply_for, use_for)

    if format_date_time is not None:
        try:
            datetime.strptime(date_time, format_date_time)

        except:
            print("\n--- Format Date Time Incorrect")
            return None

        try:
            return str(datetime.strptime(date_time, "%Y-%m-%d").strftime('%A').upper())

        except Exception as e:
            print("\n--- Exception when convert Date Time to Timestamp: " + str(e))
            return None

    return None


def get_month_of_year_by_date_time(date_time, apply_for, use_for):
    format_date_time = get_format_date_time(apply_for, use_for)

    if format_date_time is not None:
        try:
            datetime.strptime(date_time, format_date_time)

        except:
            print("\n--- Format Date Time Incorrect")
            return None

        try:
            return str(datetime.strptime(date_time, "%Y-%m-%d").strftime('%m'))

        except Exception as e:
            print("\n--- Exception when convert Date Time to Timestamp: " + str(e))
            return None

    return None


def pagination(instances=None, results_per_page=10, page=1, model=None, record_user=None):
    if type(instances) == dict:
        data = instances
        page_num = 1
        total_pages = 1
        num_results = 1
    else:
        num_results = len(instances)
        try:
            results_per_page = int(results_per_page)
        except:
            return 0
        try:
            page_num = int(page)
        except:
            return 0
        if (results_per_page is None or results_per_page <= 0) or (page_num is None or page_num <= 0):
            results_per_page = 10
            page_num = 1
            start = 0
            end = num_results
            total_pages = 1
        else:
            start = (page_num - 1) * results_per_page
            end = min(num_results, start + results_per_page)
            total_pages = int(math.ceil(num_results / results_per_page))

        if model == 'account':
            data = [format_data_account(x) for x in instances[start:end]]
        elif model == 'document':
            data = []
            for x in instances[start:end]:
                if x.document_parent_id is None:
                    data.append(format_data_document(x, record_user))
            # data = [format_data_document(x, record_user) for x in instances[start:end] if x.document_parent_id is None else True]
        else:
            data = [format_data(x) for x in instances[start:end]]

    return dict(result=data, page=page_num, total_pages=total_pages, num_results=num_results)


def auto_generate_anything(length):
    hashids = Hashids(salt="allara",
                      alphabet="ABCDEFGHIJKLMNPQRSTUVWXYZ123456789", min_length=length)

    return hashids.encode(math.floor(datetime.today().timestamp() * 100000))


def generate_password(lenght):
    letter_and_digits = string.ascii_letters + string.digits
    passw = ''.join(random.choice(letter_and_digits) for i in range(lenght))
    return passw
