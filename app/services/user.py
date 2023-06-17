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


class UserService(BaseService):
    def __init__(self):
        super(UserService, self).__init__()

    def find_by_username(self, username=""):
        query_dict = {
            "filter": {
                "username": "{username}".format(username=username)
            }
        }
        data = super().fetch_list(query_dict=query_dict, to_dict=False)
        if data["total"] == 0:
            return None
        return data['items'][0]

    def find_by_username_password(self, data):
        data['password'] = str2md5(data['password'] + data['username'])
        result = super().find_one(data, to_dict=True)
        if result is not None:
            del result['password']
            del result['id']
        return result

    def get_info(self, username):
        query = dict()
        query['username'] = username
        result = super().find_one(query, to_dict=True)
        if result is not None:
            del result['password']
            del result['id']
            result['roles'] = result['roles'].split(',')
            result['name'] = result['username']
            result['avatar'] = 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'
            result['introduction'] = 'I am a super administrator'
        return result

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)