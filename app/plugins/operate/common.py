# coding:utf-8

__author__ = 'ti'

import time
import os
from io import BytesIO
from app.ext import serv
from app.utils.utils import export
from flask import session


@export("HookGlobal")
def operate_rewrite_data(data, *args, **kwargs):
    """
    批量导入时处理数据
    :param data:
    :param args:
    :param kwargs:
    :return:
    """
    info = args[0]
    if '__uid__' in info['columns_list']:
        dataScope = session['userinfo']['dataScope']
        uid = session['userinfo']['userId']
        if dataScope == 3:
            if 'and' not in data["filter"]:
                data["filter"]['and'] = {}
            # if 'must' not in data["filter"]['bool']:
            #     data["filter"]['bool']["must"] = []
            data["filter"]["and"]["__uid__"] = uid

    return data

