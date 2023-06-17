# coding:utf-8

__author__ = 'Ti'

import json
import datetime
from app.utils.utils import export, checkip
from app.exception import TypeValueError


@export("String")
def f_string(str_, *args, **kwargs):
    try:
        return str(str_)
    except ValueError:
        raise TypeValueError("字符串格式不正确")


@export("Ip")
def f_ip(str_, *args, **kwargs):
    try:
        ok = checkip(str_)
        if ok:
            return str(str_)
        else:
            raise TypeValueError("%s的ip格式不正确" % str_)
    except ValueError:
        raise TypeValueError("%s的ip格式不正确" % str_)


@export("Auto")
def f_auto(str_, *args, **kwargs):
    try:
        if not str_:
            return ""
        return str(str_)
    except ValueError:
        raise TypeValueError("字符串格式不正确")


@export("Reverse")
def f_reverse(str_, *args, **kwargs):
    try:
        if not str_:
            return ""
        return str(str_)
    except ValueError:
        raise TypeValueError("字符串格式不正确")


@export("Group")
def f_group(str_, *args, **kwargs):
    try:
        if not str_:
            return ""
        return str(str_)
    except ValueError:
        raise TypeValueError("字符串格式不正确 str:" + str(str_))


@export("Integer")
def f_integer(str_, *args, **kwargs):
    try:
        if not str_:
            return 0
        return int(str_)
    except ValueError:
        raise TypeValueError("整型格式不正确 str:" + str(str_))


@export("Float")
def f_float(str_, *args, **kwargs):
    try:
        if str_ in [None, "", "None"]:
            return float(0)
        return float(str_)
    except ValueError:
        raise TypeValueError("浮点型格式不正确 str:" + str(str_))


@export("Date")
def f_date(str_, *args, **kwargs):
    try:
        t_format = kwargs.get("format", "%Y-%m-%d %H:%M:%S")
        if not t_format:
            t_format = "%Y-%m-%d %H:%M:%S"

        if isinstance(str_, datetime.datetime):
            return str_.strftime(t_format)

        if str_ in [None, "", "None"]:
            return None

        str_arr = str_.split('.')
        if len(str_arr) == 3:
            datetime.datetime.strptime(str_, "%Y.%m.%d")
            return str_

        datetime.datetime.strptime(str_, t_format)
        return str_
    except ValueError:
        raise TypeValueError("时间:" + str_ + " 格式不正确")


@export("File")
def f_file(str_, *args, **kwargs):
    try:
        if not str_:
            return str("")
        return str(str_)
    except ValueError:
        raise TypeValueError("File格式不正确 str:" + str(str_))


@export("Table")
def f_table(str_, *args, **kwargs):
    try:
        if str_ in [None, "", "None"]:
            return ["", []]

        if isinstance(str_, list):
            return str_

        if isinstance(str_, str):
            str_ = str_.strip()
            data = str_.replace('\'', '"')
            if len(str_) >= 7 and str_[0] == '[' and str_[len(str_)-1] == ']':
                data = json.loads(data)
                if isinstance(data, list) and len(data) == 2 and isinstance(data[1], list):
                    return data
                else:
                    raise TypeValueError("Table json格式不正确")
            else:
                return [str_, []]

        raise TypeValueError("Table格式不正确")
    except ValueError:
        raise TypeValueError("Table json格式不正确 str:" + str(str_))
