# coding=utf-8


from app.ext import serv
from app.utils.responses import response_with
from app.utils import responses as resp
from app.utils.jwt import Jwt
from .base import *
from app.config import cfg
import json

__author__ = 'Ti'


url_prefix = cfg.APP_BASE_API + "roles"
view_name = os.path.basename(__file__).split('.')[0]
view = Blueprint(view_name, __name__)
view.before_request(Jwt.load_api)


@view.route('/pages', methods=['GET'])
def page():
    data = serv.role.pages()
    test = {
        "list": [
            {
                "id": "2",
                "name": "系统管理员",
                "code": "ADMIN",
                "status": 1,
                "sort": 1,
                "createTime": "2021-03-25 12:39:54",
                "updateTime": "2022-11-05 00:22:02"
            },
            {
                "id": "3",
                "name": "访问游客",
                "code": "GUEST",
                "status": 1,
                "sort": 3,
                "createTime": "2021-05-26 15:49:05",
                "updateTime": "2019-05-05 16:00:00"
            }
        ],
        "total": 2
    }
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/options', methods=['GET'])
def options():
    data = serv.role.options()
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/<int:rid>/get', methods=['GET'])
def get(rid):
    data = serv.role.get(rid)
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    serv.role.add(data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/<int:rid>/edit', methods=['PUT'])
def edit(rid):
    data = request.get_json()
    serv.role.edit(rid, data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/<int:rid>/delete', methods=['DELETE'])
def delete(rid):
    serv.role.delete(rid)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


# 获取角色拥有的资源ID集合
@view.route('/<int:rid>/menuIds', methods=['GET'])
def menu_ids_get(rid):
    data = serv.role.get(rid)
    menus = []
    if data['menus']:
        menus = data['menus']
    return response_with(resp.SUCCESS_20000, value={"data": menus})


# 更新角色拥有的资源ID集合
@view.route('/<int:rid>/menus/edit', methods=['POST', 'PUT'])
def menus_ids_edit(rid):
    data = request.get_json()
    serv.role.edit_menu(rid, data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})
