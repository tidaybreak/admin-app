# coding=utf-8


from app.ext import serv
from app.utils.responses import response_with
from app.utils import responses as resp
from app.utils.jwt import Jwt
from .base import *
from app.config import cfg
import json

__author__ = 'Ti'

url_prefix = cfg.APP_BASE_API + "users"
view_name = os.path.basename(__file__).split('.')[0]
view = Blueprint(view_name, __name__)
view.before_request(Jwt.load_api)


@view.route('/info', methods=['GET'])
@view.route('/me', methods=['GET'])
def me_info():
    userinfo = Jwt.payload()
    result = serv.user.get_info(userinfo['username'])
    return response_with(resp.SUCCESS_20000, value={"data": result})


@view.route('/pages', methods=['GET'])
def pages():
    data = serv.user.pages()
    test = {
        "list": [
            {
                "id": 0,
                "username": "admin",
                "nickname": "系统管理员",
                "mobile": "17621210123",
                "genderLabel": "男",
                "avatar": "https://s2.loli.net/2022/04/07/gw1L2Z5sPtS8GIl.gif",
                "email": '',
                "status": 1,
                "deptName": "研发部门",
                "roleNames": "系统管理员",
                "createTime": "2023-04-11"
            }
        ],
        "total": 1
    }
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/logout', methods=['POST'])
def logout():
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/<int:uid>/get', methods=['GET'])
def get(uid):
    data = serv.user.get(uid)
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    serv.user.add(data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/<int:uid>/edit', methods=['PUT'])
def edit(uid):
    data = request.get_json()
    serv.user.edit(uid, data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/<int:uid>/delete', methods=['DELETE'])
def delete(uid):
    serv.user.delete(uid)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/<int:uid>/password', methods=['PATCH'])
def update_password(uid):
    password = request.args.get('password')
    serv.user.update_password(uid, password)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/<int:uid>/status', methods=['PATCH'])
def update_status(uid):
    status = int(request.args.get('status'))
    data = {
        "status": status
    }
    serv.user.edit(uid, data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/template', methods=['GET'])
def template():
    #serv.user.delete(uid)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/_export', methods=['GET'])
def _export():
    #serv.user.delete(uid)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/_import', methods=['GET'])
def _import():
    #serv.user.delete(uid)
    return response_with(resp.SUCCESS_20000, value={"data": {}})