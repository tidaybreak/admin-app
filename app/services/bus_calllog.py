__author__ = 'Ti'

from app.services.base import BaseService
from passlib.hash import pbkdf2_sha256 as sha256
from app.utils.utils import str2md5
from flask import session
import datetime


class CalllogService(BaseService):
    def __init__(self):
        super(CalllogService, self).__init__()

    def pages(self, query_dict, page=1, limit=None):
        data = super().fetch_list(query_dict=query_dict, page=page, limit=limit, to_type="dict", field_info=True)
        return data

    def get(self, id):
        query = dict()
        query['sn'] = id
        result = super().find_one(query, to_type="dict")
        return result

    def add(self, data):
        return self.insert(data)

    def edit(self, rid, data):
        query_dict = {
            "sn": rid
        }
        return super().update(query_dict=query_dict, update_dict=data, insert=False)

    def delete(self, rid):
        return super().delete(rid)

    def download(self, data):
        new_data = []
        for sn in data:
            new_data.append({
                "sn": sn,
                "download_time": datetime.datetime.now()
            })
        return super().bulk_update(new_data)
