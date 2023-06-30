__author__ = 'Ti'

import re
import os
import filecmp
import tempfile
from app.ext import serv, cache
from app.ext import sup_ctr
from app.services.base import BaseService
from jinja2 import Environment, FileSystemLoader
from passlib.hash import pbkdf2_sha256 as sha256
from app.utils.utils import str2md5
from app.utils.jwt import Jwt
from flask import session


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
        if result is None:
            return result

        # 数据源权限默认个人3，有多个取最高的0
        result['dataScope'] = []
        for ent in result['roleIds']:
            role = serv.role.get(ent)
            if role and role['dataScope'] is not None and role['dataScope'] >= 0:
                result['dataScope'].append(role['dataScope'])
        if len(result['dataScope']) == 0:
            result['dataScope'] = [3]
        result['dataScope'].sort()
        result['dataScope'] = result['dataScope'][0]
        return result

    def update_password(self, id, password):
        query = dict()
        query['id'] = id
        result = super().find_one(query, to_type="dict")

        password = str2md5(password + result['username'])
        self.edit(id, {"password": password})
        return result

    def get_token(self, data):
        result = self.find_by_username_password(data)
        if result is None:
            return {"msg": '用户名或密码错误'}
        else:
            # loginTime = datetime.datetime.utcnow()
            # self.admin.update_one(result['username'],{'loginTime':loginTime})
            jwtdata = {'username': result['username'], 'roles': result['roleIds']}
            data = {
                "access_token": Jwt.jwtEncode(jwtdata).decode('utf-8'),
                "token_type": "bearer",
                "refresh_token": "",
                "expires_in": 3599,
                "scope": "all",
                "deptId": result['deptId'],
                "dataScope": result['dataScope'],
                "userId": result['id'],
                "username": result['username'],
                'dataScope': result['dataScope']
                #"jti": "bbj-qLJWcWhb9O8nOSZIhuvJftk"
            }
            session['userinfo'] = data
            return {"data": data}

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

    @cache.memoize(timeout=120)
    def select_user(self):
        result = []
        query_dict = {}
        data = super().fetch_list(query_dict=query_dict, to_type="dict")
        if data["total"] == 0:
            return []
        for ent in data['items']:
            result.append([
                ent["id"], ent["username"]
            ])
        return result