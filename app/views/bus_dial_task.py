# coding=utf-8


from app.ext import serv
from app.utils.responses import response_with
from app.utils import responses as resp
from app.utils.jwt import Jwt
from .base import *
from app.config import cfg
from flask import session
from datetime import datetime, timedelta
import json

__author__ = 'Ti'


url_prefix = cfg.APP_BASE_API + "dialtask"
view_name = os.path.basename(__file__).split('.')[0]
view = Blueprint(view_name, __name__)
view.before_request(Jwt.load_api)


@view.route('/pages', methods=['GET', 'POST'])
def query():
    # sess = Jwt.payload()
    data = request.get_json()
    query_dict = data['search']
    result = serv.bus_dialtask.pages(query_dict, page=data['pageNum'], limit=data['pageSize'], field_info=data['columns_info'])

    return response_with(resp.SUCCESS_20000, value={"data": result})


@view.route('/<uid>/get', methods=['GET'])
def get(uid):
    data = serv.bus_dialtask.get(uid)
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    serv.bus_dialtask.add(data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/<uid>/edit', methods=['PUT'])
def edit(uid):
    data = request.get_json()
    serv.bus_dialtask.edit(uid, data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/<uid>/delete', methods=['DELETE'])
def delete(uid):
    serv.bus_dialtask.delete(uid)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    serv.bus_dialtask.download(data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})