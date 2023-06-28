__author__ = 'Ti'

import re
import os
import filecmp
import tempfile
from app.ext import serv
from app.ext import sup_ctr
from app.services.base import BaseService
from jinja2 import Environment, FileSystemLoader
from passlib.hash import pbkdf2_sha256 as sha256
from app.utils.utils import str2md5


class RoleService(BaseService):
    def __init__(self):
        super(RoleService, self).__init__()

    def pages(self, page=1, limit=None):
        query_dict = {}
        data = super().fetch_list(query_dict=query_dict, page=page, limit=limit, to_type="dict")
        return data

    def options(self):
        query_dict = {}
        result = []
        data = super().fetch_list(query_dict=query_dict, to_type="dict")
        for ent in data['items']:
            result.append({
                "value": ent['id'],
                "label": ent['name']
            })
        return result

    def role_id_map(self):
        query_dict = {}
        data = super().fetch_list(query_dict=query_dict, to_type="map.id")
        return data

    def role_code_map(self):
        query_dict = {}
        data = super().fetch_list(query_dict=query_dict, to_type="map.code")
        return data

    def get(self, id):
        query = dict()
        query['id'] = id
        result = super().find_one(query, to_type="dict")
        return result

    def add(self, data):
        return self.insert(data)

    def edit(self, rid, data):
        query_dict = {
            "id": rid
        }
        # 在资源分配中修改
        del data['menus']
        return super().update(query_dict=query_dict, update_dict=data, insert=False)

    def delete(self, rid):
        return super().delete(rid)

    def edit_menu(self, rid, menus):
        query_dict = {
            "id": rid
        }
        menus = [str(item) for item in menus]
        update_dict = {
            "menus": ','.join(menus)
        }
        return super().update(query_dict=query_dict, update_dict=update_dict, insert=False)

    # 目录id对应role信息
    def get_menus_role(self):
        query_dict = {}
        result = {}
        data = super().fetch_list(query_dict=query_dict, to_type="dict")
        for ent in data['items']:
            for mid in ent['menus']:
                if mid not in result:
                    result[mid] = []
                result[mid] += [ent['code']]
        return result

    # 目录id对应perm权限列表
    def get_menus_perm(self):
        query_dict = {}
        result = {}
        data = super().fetch_list(query_dict=query_dict, to_type="dict")
        roles = serv.menu.menu_id_map()
        for ent in data['items']:
            for mid in ent['menus']:
                if mid in roles:
                    if roles[mid]['perm'] is not None and roles[mid]['perm'] != '':
                        if mid not in result:
                            result[mid] = []
                        result[mid] += [roles[mid]['perm']]
        return result
