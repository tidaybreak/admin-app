# coding=utf-8

import os
from app.ext import serv
from app.utils.utils import res_json
from celery import chain
from app.utils.responses import response_with
from app.utils import responses as resp
from app.utils.jwt import Jwt
from flask import Blueprint, current_app, request
from app.config import cfg
import json

__author__ = 'Ti'


url_prefix = ""
view_name = os.path.basename(__file__).split('.')[0]
view = Blueprint(view_name, __name__)


@view.route("/check")
def check():
    return "ok"


@view.route("/version")
def version():
    ver = open(os.path.join(current_app.root_path, "version")).read()
    return ver


@view.route(cfg.APP_BASE_API + '/user/login', methods=['POST'])
def authenticate_login():
    data = request.get_json()
    result = serv.user.find_by_username_password(data)
    if result is None:
        return response_with(resp.UNAUTHORIZED_401)
    else:
        # loginTime = datetime.datetime.utcnow()
        # self.admin.update_one(result['username'],{'loginTime':loginTime})
        jwtdata = {'username': result['username'], 'roles': result['roles']}
        return response_with(resp.SUCCESS_20000, value={"data": {'token': Jwt.jwtEncode(jwtdata).decode('utf-8')}})
        # return response(data, code=20000, message='登陆成功！')


@view.route('/list', methods=['GET'])
def authenticate_list():
    p = Jwt.authHeader(request)
    res = json.loads(p)
    if res['code'] == 20000:
        data = {
            "total": 1,
            "items": [{
                "order_no": "C6516F0C-DC2F-aEc9-7A15-9DD55F4e7A4B",
                "timestamp": 159482548419,
                "username": "Laura Thomas",
                "price": 13183,
                "status": "success"
            }]
        }
        return response_with(resp.SUCCESS_20000, value={"data": data})
    else:
        return p
