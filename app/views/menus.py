# coding=utf-8


from app.ext import serv
from app.utils.responses import response_with
from app.utils import responses as resp
from app.utils.jwt import Jwt
from .base import *
from app.config import cfg
import json

__author__ = 'Ti'


url_prefix = cfg.APP_BASE_API + "menus"
view_name = os.path.basename(__file__).split('.')[0]
view = Blueprint(view_name, __name__)
view.before_request(Jwt.load_api)


@view.route('/routes', methods=['GET'])
def route():
    data = serv.menu.tree(type="route")
    test = [{
                                 "path": "/system",
                                 "component": "Layout",
                                 "redirect": "/system/user",
                                 "meta": {
                                     "title": "系统管理",
                                     "icon": "system",
                                     "hidden": False,
                                     "alwaysShow": True,
                                     "roles": [
                                         "ADMIN"
                                     ],
                                     "keepAlive": True
                                 },
                                 "children": [
                                     {
                                         "path": "user",
                                         "component": "system/user/index",
                                         "name": "user",
                                         "meta": {
                                             "title": "用户管理",
                                             "icon": "user",
                                             "hidden": False,
                                             "alwaysShow": False,
                                             "roles": [
                                                 "ADMIN"
                                             ],
                                             "keepAlive": True
                                         }
                                     },
                                     {
                                         "path": "role",
                                         "component": "system/role/index",
                                         "name": "role",
                                         "meta": {
                                             "title": "角色管理",
                                             "icon": "role",
                                             "hidden": False,
                                             "alwaysShow": False,
                                             "roles": [
                                                 "ADMIN"
                                             ],
                                             "keepAlive": True
                                         }
                                     },
                                     {
                                         "path": "cmenu",
                                         "component": "system/menu/index",
                                         "name": "cmenu",
                                         "meta": {
                                             "title": "菜单管理",
                                             "icon": "menu",
                                             "hidden": False,
                                             "alwaysShow": False,
                                             "roles": [
                                                 "ADMIN"
                                             ],
                                             "keepAlive": True
                                         }
                                     },
                                     {
                                         "path": "dept",
                                         "component": "system/dept/index",
                                         "name": "dept",
                                         "meta": {
                                             "title": "部门管理",
                                             "icon": "tree",
                                             "hidden": False,
                                             "alwaysShow": False,
                                             "roles": [
                                                 "ADMIN"
                                             ],
                                             "keepAlive": True
                                         }
                                     },
                                     {
                                         "path": "dict",
                                         "component": "system/dict/index",
                                         "name": "dict",
                                         "meta": {
                                             "title": "字典管理",
                                             "icon": "dict",
                                             "hidden": False,
                                             "alwaysShow": False,
                                             "roles": [
                                                 "ADMIN"
                                             ],
                                             "keepAlive": True
                                         }
                                     },
                                     {
                                         "path": "client",
                                         "component": "system/client/index",
                                         "name": "client",
                                         "meta": {
                                             "title": "客户端管理",
                                             "icon": "client",
                                             "hidden": False,
                                             "alwaysShow": False,
                                             "roles": [
                                                 "ADMIN"
                                             ],
                                             "keepAlive": True
                                         }
                                     }
                                 ]
                             }]
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/pages', methods=['GET'])
def pages():
    data = serv.menu.tree(type="pages")
    test = [
        {
            "id": "1",
            "parentId": "0",
            "name": "系统管理",
            "icon": "system",
            "routeName": "",
            "routePath": "",
            "component": "Layout",
            "sort": 1,
            "visible": 1,
            "redirect": "/system/user",
            "type": "CATALOG",
            "children": [
                {
                    "id": "2",
                    "parentId": "1",
                    "name": "用户管理",
                    "icon": "user",
                    "routeName": "",
                    "routePath": "",
                    "component": "system/user/index",
                    "sort": 1,
                    "visible": 1,
                    "redirect": "",
                    "type": "MENU",
                    "children": [
                        {
                            "id": "40",
                            "parentId": "2",
                            "name": "新增用户",
                            "icon": "",
                            "routeName": "",
                            "routePath": "",
                            "component": "",
                            "sort": 1,
                            "visible": 1,
                            "redirect": "",
                            "type": "BUTTON",
                            "children": [],
                            "perm": "sys:user:add",
                            "createTime": "",
                            "updateTime": ""
                        },
                        {
                            "id": "41",
                            "parentId": "2",
                            "name": "修改用户",
                            "icon": "",
                            "routeName": "",
                            "routePath": "",
                            "component": "",
                            "sort": 2,
                            "visible": 1,
                            "redirect": "",
                            "type": "BUTTON",
                            "children": [],
                            "perm": "sys:user:edit",
                            "createTime": "2022-11-05 01:26:44",
                            "updateTime": "2022-11-05 01:26:44"
                        },
                        {
                            "id": "42",
                            "parentId": "2",
                            "name": "删除用户",
                            "icon": "",
                            "routeName": "",
                            "routePath": "",
                            "component": "",
                            "sort": 3,
                            "visible": 1,
                            "redirect": "",
                            "type": "BUTTON",
                            "children": [],
                            "perm": "sys:user:del",
                            "createTime": "2022-11-05 01:27:13",
                            "updateTime": "2022-11-05 01:27:13"
                        }
                    ],
                    "perm": "",
                    "createTime": "2021-08-28 09:12:21",
                    "updateTime": "2021-08-28 09:12:21"
                },
                {
                    "id": "3",
                    "parentId": "1",
                    "name": "角色管理",
                    "icon": "role",
                    "routeName": "",
                    "routePath": "",
                    "component": "system/role/index",
                    "sort": 2,
                    "visible": 1,
                    "redirect": "",
                    "type": "MENU",
                    "children": [],
                    "perm": "",
                    "createTime": "2021-08-28 09:12:21",
                    "updateTime": "2021-08-28 09:12:21"
                },
                {
                    "id": "4",
                    "parentId": "1",
                    "name": "菜单管理",
                    "icon": "menu",
                    "routeName": "",
                    "routePath": "",
                    "component": "system/menu/index",
                    "sort": 3,
                    "visible": 1,
                    "redirect": "",
                    "type": "MENU",
                    "children": [],
                    "perm": "",
                    "createTime": "2021-08-28 09:12:21",
                    "updateTime": "2021-08-28 09:12:21"
                },
                {
                    "id": "5",
                    "parentId": "1",
                    "name": "部门管理",
                    "icon": "tree",
                    "routeName": "",
                    "routePath": "",
                    "component": "system/dept/index",
                    "sort": 4,
                    "visible": 1,
                    "redirect": "",
                    "type": "MENU",
                    "children": [],
                    "perm": "",
                    "createTime": "2021-08-28 09:12:21",
                    "updateTime": "2021-08-28 09:12:21"
                },
                {
                    "id": "6",
                    "parentId": "1",
                    "name": "字典管理",
                    "icon": "dict",
                    "routeName": "",
                    "routePath": "",
                    "component": "system/dict/index",
                    "sort": 5,
                    "visible": 1,
                    "redirect": "",
                    "type": "MENU",
                    "children": [],
                    "perm": "",
                    "createTime": "2021-08-28 09:12:21",
                    "updateTime": "2021-08-28 09:12:21"
                },
                {
                    "id": "7",
                    "parentId": "1",
                    "name": "客户端管理",
                    "icon": "client",
                    "routeName": "",
                    "routePath": "",
                    "component": "system/client/index",
                    "sort": 6,
                    "visible": 1,
                    "redirect": "",
                    "type": "MENU",
                    "children": [],
                    "perm": "",
                    "createTime": "2021-08-28 09:12:21",
                    "updateTime": "2021-08-28 09:12:21"
                }
            ],
            "perm": "",
            "createTime": "2021-08-28 09:12:21",
            "updateTime": "2021-08-28 09:12:21"
        }
    ]
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/options', methods=['GET'])
def options():
    data = serv.menu.tree(type="options")
    test = [
    ]
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/resources', methods=['GET'])
def resources():
    data = serv.menu.tree(type="options")
    test = [
    ]
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/<int:mid>/get', methods=['GET'])
def get(mid):
    data = serv.menu.get(mid)
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    serv.menu.add(data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/<int:mid>/edit', methods=['PUT'])
def edit(mid):
    data = request.get_json()
    serv.menu.edit(mid, data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/<int:mid>/delete', methods=['DELETE'])
def delete(mid):
    serv.menu.delete(mid)
    return response_with(resp.SUCCESS_20000, value={"data": {}})