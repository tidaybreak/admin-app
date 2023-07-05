__author__ = 'Ti'

from app.services.base import BaseService
from app.utils import utils as utils
from app.utils.ciopaas import ciopaas as ciopaaas
from app.jobs.aicrm import fun_dailtask
from app.ext import serv, cache
from app.config import cfg
import datetime, os, time


class BusDialtaskService(BaseService):
    def __init__(self):
        super(BusDialtaskService, self).__init__()

    def pages(self, query_dict={
                                "filter": {
                                }
                            }, page=1, limit=None, field_info=True):
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

    def get_api_by_uid(self, uid):
        user = serv.user.get(uid)
        if user is None:
            return None
        api = serv.dict.get_dict('API', user['username'])
        if api is None:
            return None
        val = api['value'].split(',')
        host = val[0]
        api_access_id = val[1]
        api_access_secret = val[2]
        return host, api_access_id, api_access_secret

    @cache.memoize(timeout=120)
    def select_child_account(self, uid):
        api = self.get_api_by_uid(uid)
        if api is None:
            return []
        data = ciopaaas.aiUserDatasapi(api[0], api[1], api[2])
        result = []
        for ent in data['data']:
            result.append([ent['user_sn'], "%s(%s)" % (ent['contact'], ent['user_name'])])
        return result

    @cache.memoize(timeout=120)
    def select_templatelist(self, uid):
        api = self.get_api_by_uid(uid)
        if api is None:
            return []
        data = ciopaaas.templatelist(api[0], api[1], api[2])
        result = []
        for ent in data['data']:
            result.append([ent['sn'], ent['project_caption']])
        return result

    def do_task(self, tasks, oper):
        for task in tasks:
            username = task[0]
            dial_task_main_id = task[1]
            api = serv.dict.get_dict('API', username)
            if api is None:
                continue
            data = ciopaaas.task_action(api, dial_task_main_id, oper)
            print(data)

            val = api['value'].split(',')
            url = val[0]
            api_access_id = val[1]
            api_access_secret = val[2]
            fun_dailtask(None, url, api_access_id, api_access_secret)
        return {}

    def add_task(self, data):
        api = self.get_api_by_uid(data['__uid__'])
        if api is None:
            return []

        file_path = os.path.join(cfg.GLOBAL_TEMP_PATH, data['tels'])
        tels = utils.parse_import_xls(file_path)
        client_info_json = {
                               "data": [
                               ]
                           }
        for ent in tels[1]:
            client_info_json['data'].append(
                {
                    #"姓名": ent[0],
                    "电话": ent[1]
                    #"地址": ent[2],
                    #"公司名称": ent[3],
                    #"备注": ent[4]
                }
            )
        #print(client_info_json)
        result = ciopaaas.addJsonOfAsync(api[0], api[1], api[2], data['source'], data['project_caption'], data['user_name'], client_info_json)
        time.sleep(5)
        fun_dailtask(data['__uid__'], api[0], api[1], api[2])
        return result