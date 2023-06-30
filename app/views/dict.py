# coding=utf-8


from app.ext import serv
from app.utils.responses import response_with
from app.utils import responses as resp
from app.utils.jwt import Jwt
from .base import *
from app.config import cfg
import json

__author__ = 'Ti'


url_prefix = cfg.APP_BASE_API + "dict"
view_name = os.path.basename(__file__).split('.')[0]
view = Blueprint(view_name, __name__)
view.before_request(Jwt.load_api)



@view.route('/types/pages', methods=['GET'])
def types_pages():
    data = serv.dict.pages(parentId=0)
    test = {
        "list": [
            {
                "id": "1",
                "name": "性别",
                "code": "gender",
                "status": 1
            },
            {
                "id": "2",
                "name": "授权方式",
                "code": "grant_type",
                "status": 1
            },
            {
                "id": "3",
                "name": "微服务列表",
                "code": "micro_service",
                "status": 1
            },
            {
                "id": "4",
                "name": "请求方式",
                "code": "request_method",
                "status": 1
            }
        ],
        "total": 4
    }
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/items/pages', methods=['GET'])
def items_pages():
    typeCode = request.args.get('typeCode')
    data = serv.dict.items_pages(typeCode=typeCode)
    test = {
        "list": [
            {
                "id": "1",
                "name": "男",
                "value": "1",
                "status": 1
            },
            {
                "id": "2",
                "name": "女",
                "value": "2",
                "status": 1
            },
            {
                "id": "3",
                "name": "未知",
                "value": "0",
                "status": 1
            }
        ],
        "total": 3
    }
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/types/<typeCode>/items', methods=['GET'])
def items(typeCode):
    data = serv.dict.items_pages(typeCode=typeCode)
    test = [
        {
            "value": "1",
            "label": "男"
        },
        {
            "value": "2",
            "label": "女"
        },
        {
            "value": "0",
            "label": "未知"
        }
    ]
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/types/<int:did>/get', methods=['GET'])
def types_get(did):
    data = serv.dict.get(did)
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/types/add', methods=['POST'])
def types_add():
    data = request.get_json()
    data['parentId'] = 0
    serv.dict.add(data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/types/<int:did>/edit', methods=['PUT'])
def types_edit(did):
    data = request.get_json()
    serv.dict.edit(did, data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/types/<int:did>/delete', methods=['DELETE'])
def types_delete(did):
    serv.dict.delete(did)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/items/<int:did>/get', methods=['GET'])
def items_get(did):
    data = serv.dict.get(did)
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/items/add', methods=['POST'])
def items_add():
    data = request.get_json()
    #data['parentId'] = 0
    serv.dict.add(data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/items/<int:did>/edit', methods=['PUT'])
def items_edit(did):
    data = request.get_json()
    serv.dict.edit(did, data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/items/<int:did>/delete', methods=['DELETE'])
def items_delete(did):
    serv.dict.delete(did)
    return response_with(resp.SUCCESS_20000, value={"data": {}})