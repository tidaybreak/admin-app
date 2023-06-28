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


class UserService(BaseService):
    def __init__(self):
        super(UserService, self).__init__()

    def find_by_username(self, username=""):
        query_dict = {
            "filter": {
                "username": "{username}".format(username=username)
            }
        }
        data = super().fetch_list(query_dict=query_dict, to_type="")
        if data["total"] == 0:
            return None
        return data['items'][0]

    def find_by_username_password(self, data):
        query = dict()
        query['password'] = str2md5(data['password'] + data['username'])
        query['username'] = data['username']
        result = super().find_one(query, to_type="dict")
        return result

    def update_password(self, id, password):
        query = dict()
        query['id'] = id
        result = super().find_one(query, to_type="dict")

        password = str2md5(password + result['username'])
        self.edit(id, {"password": password})
        return result

    def get_info(self, username):
        query = dict()
        query['username'] = username
        result = super().find_one(query, to_type="dict")
        if result is None:
            return None

        user_info = {
            "userId": result['id'],
            "nickname": result['nickname'],
            "avatar": result['avatar'],
            "roles": [],
            "perms": []
        }
        roles = serv.role.role_id_map()
        perms = serv.role.get_menus_perm()
        for rid in result['roleIds']:
            if rid in roles:
                user_info['roles'] += [roles[rid]['code']]
                for mid in roles[rid]['menus']:
                    if mid in perms:
                        user_info['perms'] += perms[mid]
        #result['roles'] = result['roles'].split(',')
        #result['name'] = result['username']
        #result['avatar'] = 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'
        #result['introduction'] = 'I am a super administrator'
        return user_info

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    def pages(self, page=1, limit=None):
        query_dict = {}
        data = super().fetch_list(query_dict=query_dict, page=page, limit=limit, to_type="dict")
        if data["total"] == 0:
            return None

        depts = serv.dept.dept_id_map()
        roles = serv.role.role_id_map()
        for ent in data['items']:
            ent['roleNames'] = []
            did = ent['deptId']
            if did in depts:
                ent['deptName'] = depts[did]['name']
            for rid in ent['roleIds']:
                if rid in roles:
                    ent['roleNames'] += [roles[rid]['name']]
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
        if 'roleIds' in data and data['roleIds']:
            data['roleIds'] = ','.join([str(item) for item in data['roleIds']])

        return super().update(query_dict=query_dict, update_dict=data, insert=False)

    def delete(self, rid):
        return super().delete(rid)
