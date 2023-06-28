__author__ = 'Ti'

import re
import os
import filecmp
import tempfile

from app.ext import sup_ctr
from app.services.base import BaseService
from jinja2 import Environment, FileSystemLoader
from passlib.hash import pbkdf2_sha256 as sha256
from app.utils.utils import str2md5


class DictService(BaseService):
    def __init__(self):
        super(DictService, self).__init__()

    def pages(self, parentId=0, page=1, limit=None):
        query_dict = {
            "filter": {
                "parentId": parentId
            }
        }
        data = super().fetch_list(query_dict=query_dict, page=page, limit=limit, to_type="dict")
        return data

    def items_pages(self, code=0, page=1, limit=None):
        query = dict()
        query['code'] = code
        result = super().find_one(query, to_type="dict")

        data = self.pages(parentId=result['id'])
        return data

    def tree(self, parent_id=0, level=0, type="pages"):
        query_dict = {}
        data = super().fetch_list(query_dict=query_dict, to_type="dict")
        if data["total"] == 0:
            return []
        data = data['items']
        return self.generate_tree(data, parent_id=parent_id, level=level, type=type)

    def generate_tree(self, data, parent_id=0, level=0, type="pages"):
        tree = []
        for item in data:
            if item['parentId'] == parent_id:
                if type == "pages":
                    node = item
                else:
                    node = {'label': item['name'], 'value': item['id']}

                children = self.generate_tree(data, item['id'], level + 1, type=type)
                if children:
                    node['children'] = children
                tree.append(node)
        return tree

    def dept_id_map(self):
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
        return super().update(query_dict=query_dict, update_dict=data, insert=False)

    def delete(self, rid):
        return super().delete(rid)
