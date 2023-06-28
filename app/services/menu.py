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


class MenuService(BaseService):
    def __init__(self):
        super(MenuService, self).__init__()

    def pages(self, page=1, limit=None):
        query_dict = {}
        data = super().fetch_list(query_dict=query_dict, page=page, limit=limit, to_type="dict")
        return data

    def routes(self):
        query_dict = {}
        data = super().fetch_list(query_dict=query_dict, to_type="dict")
        return data

    def tree(self, parent_id=0, level=0, type="pages"):
        query_dict = {
        }
        if type == "route":
            query_dict = {
                "filter": {
                    "type": {
                                "in": ["CATALOG", "MENU"]
                              }
                }
            }
        data = super().fetch_list(query_dict=query_dict, to_type="dict")
        if data["total"] == 0:
            return []
        data = data['items']

        menus_role = serv.role.get_menus_role()
        return self.generate_tree(data, parent_id=parent_id, level=level, type=type, menus_role=menus_role)

    def generate_tree(self, data, parent_id=0, level=0, type="pages", menus_role={}):
        tree = []
        for item in data:
            if item['parentId'] == parent_id:
                # node = {'name': item['name'], 'value': item['id']}
                if type == "route":
                    node = {
                        "path": item['path'],
                        "component": item['component'],
                        "name": item['path'],
                        "meta": {
                            "title": item['name'],
                            "icon": item['icon'],
                            "hidden": item['hidden'],
                            "alwaysShow": item['alwaysShow'],
                            "roles": [
                            ],
                            "keepAlive": item['keepAlive']
                        }
                    }
                    if item['redirect']:
                        node['redirect'] = item['redirect']
                    if item['id'] in menus_role:
                        node["meta"]['roles'] = menus_role[item['id']]
                elif type == "options":
                    node = {'label': item['name'], 'value': item['id']}
                else:
                    node = item
                children = self.generate_tree(data, item['id'], level + 1, type=type, menus_role=menus_role)
                if children:
                    node['children'] = children
                tree.append(node)
        return tree

    def menu_id_map(self):
        query_dict = {}
        data = super().fetch_list(query_dict=query_dict, to_type="map")
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
        update_dict = data
        return super().update(query_dict=query_dict, update_dict=data, insert=False)

    def delete(self, rid):
        return super().delete(rid)
