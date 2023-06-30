__author__ = 'Ti'

from app.services.base import BaseService
from passlib.hash import pbkdf2_sha256 as sha256
from app.utils.utils import str2md5
from flask import session
import datetime
from app.ext import serv, cache
from app.utils.ciopaas.ciopaas import get_user_list


class BusDialtaskService(BaseService):
    def __init__(self):
        super(BusDialtaskService, self).__init__()

    def pages(self, query_dict, page=1, limit=None, field_info=True):
        data = super().fetch_list(query_dict=query_dict, page=page, limit=limit, to_type="dict", field_info=field_info)
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

    def task_update(self, data):
        new_data = []
        for sn in data['data']['list']:
            new_data.append({
                "sn": sn,
                "download_time": datetime.datetime.now()
            })
        return super().bulk_update(new_data)

    @cache.memoize(timeout=120)
    def select_child_account(self, uid):
        user = serv.user.get(uid)
        if user is None:
            return []
        api = serv.dict.get_dict('API', user['username'])
        if api is None:
            return []
        data = get_user_list(api)
        result = []
        for ent in data['data']:
            result.append([ent['user_name'], "%s(%s)" % (ent['contact'], ent['user_name'])])
        return result