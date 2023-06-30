__author__ = 'Ti'

from app.services.base import BaseService
from passlib.hash import pbkdf2_sha256 as sha256
from app.utils.utils import str2md5
from flask import session
import datetime
from app.ext import serv, cache
from app.utils.ciopaas.ciopaas import get_user_list, task_action
from app.jobs.aicrm import func_api, fun_dailtask


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

    def do_task(self, tasks, oper):
        for task in tasks:
            uid = task[0]
            dial_task_main_id = task[1]
            user = serv.user.get(uid)
            if user is None:
                continue
            api = serv.dict.get_dict('API', user['username'])
            if api is None:
                continue
            data = task_action(api, dial_task_main_id, oper)
            print(data)

        func_api(fun_dailtask)
        return {}
