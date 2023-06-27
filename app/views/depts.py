# coding=utf-8


from app.ext import serv
from app.utils.responses import response_with
from app.utils import responses as resp
from app.utils.jwt import Jwt
from .base import *
from app.config import cfg
import json

__author__ = 'Ti'


url_prefix = cfg.APP_BASE_API + "dept"
view_name = os.path.basename(__file__).split('.')[0]
view = Blueprint(view_name, __name__)
view.before_request(Jwt.load_api)


@view.route('/pages', methods=['GET'])
def pages():
    data = serv.dept.tree(type="pages")
    test = [
        {
            "id": "1",
            "parentId": "0",
            "name": "有来技术",
            "treePath": "0",
            "sort": 1,
            "status": 1,
            "leader": "",
            "mobile": "",
            "email": "",
            "children": [
                {
                    "id": "2",
                    "parentId": "1",
                    "name": "研发部门",
                    "treePath": "0,1",
                    "sort": 1,
                    "status": 1,
                    "leader": "",
                    "mobile": "",
                    "email": "",
                    "children": [],
                    "createTime": "",
                    "updateTime": "2022-04-19 12:46:37"
                },
                {
                    "id": "3",
                    "parentId": "1",
                    "name": "测试部门",
                    "treePath": "0,1",
                    "sort": 1,
                    "status": 1,
                    "leader": "",
                    "mobile": "",
                    "email": "",
                    "children": [],
                    "createTime": "",
                    "updateTime": "2022-04-19 12:46:37"
                }
            ],
            "createTime": "",
            "updateTime": ""
        }
    ]
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/options', methods=['GET'])
def options():
    data = serv.dept.tree(type="options")
    test = [
        {
            "value": "1",
            "label": "有来技术",
            "children": [
                {
                    "value": "2",
                    "label": "研发部门"
                },
                {
                    "value": "3",
                    "label": "测试部门"
                }
            ]
        }
    ]
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/<int:did>/get', methods=['GET'])
def get(did):
    data = serv.dept.get(did)
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    serv.dept.add(data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/<int:did>/edit', methods=['PUT'])
def edit(did):
    data = request.get_json()
    serv.dept.edit(did, data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/<int:did>/delete', methods=['DELETE'])
def delete(did):
    serv.dept.delete(did)
    return response_with(resp.SUCCESS_20000, value={"data": {}})
