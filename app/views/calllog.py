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


url_prefix = cfg.APP_BASE_API + "calllog"
view_name = os.path.basename(__file__).split('.')[0]
view = Blueprint(view_name, __name__)
view.before_request(Jwt.load_api)


@view.route('/pages', methods=['GET', 'POST'])
def query():
    # sess = Jwt.payload()
    data = request.get_json()
    query_dict = data['search']
    result = serv.calllog.pages(query_dict, page=data['pageNum'], limit=data['pageSize'])

    test = {
        "total": 2,
        "items": [
            {
                "id": 1,
                "timestamp": 551310858270,
                "author": "Anthony",
                "reviewer": "Dorothy",
                "title": "Hmsvt Qknjttzj Bfxxkcdy Gvexce Vjtlvduhk Lpod Oagbkg Glglc Bnabrisyy Liqwxdur",
                "content_short": "mock data",
                "content": "<p>I am testing data, I am testing data.</p><p><img src=\"https://wpimg.wallstcn.com/4c69009c-0fd4-4153-b112-6cb53d1cf943\"></p>",
                "forecast": 15.66,
                "importance": 1,
                "type": "US",
                "status": "draft",
                "display_time": "1977-06-17 04:21:41",
                "comment_disabled": True,
                "pageviews": 670,
                "image_uri": "https://wpimg.wallstcn.com/e4558086-631c-425c-9430-56ffb46e70b3",
                "platforms": [
                    "a-platform"
                ]
            },
            {
                "id": 2,
                "timestamp": 152884831414,
                "author": "Karen",
                "reviewer": "Christopher",
                "title": "Ptrorhbj Pcicwbwtcp Urtd Huvbpdt Uxmpbwex Kcqna Ghskhfchw Uczncdy",
                "content_short": "mock data",
                "content": "<p>I am testing data, I am testing data.</p><p><img src=\"https://wpimg.wallstcn.com/4c69009c-0fd4-4153-b112-6cb53d1cf943\"></p>",
                "forecast": 38.15,
                "importance": 3,
                "type": "CN",
                "status": "draft",
                "display_time": "2000-09-08 05:08:38",
                "comment_disabled": True,
                "pageviews": 3346,
                "image_uri": "https://wpimg.wallstcn.com/e4558086-631c-425c-9430-56ffb46e70b3",
                "platforms": [
                    "a-platform"
                ]
            }]
    }
    return response_with(resp.SUCCESS_20000, value={"data": result})


@view.route('/<uid>/get', methods=['GET'])
def get(uid):
    data = serv.calllog.get(uid)
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    serv.calllog.add(data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/<uid>/edit', methods=['PUT'])
def edit(uid):
    data = request.get_json()
    serv.calllog.edit(uid, data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/<uid>/delete', methods=['DELETE'])
def delete(uid):
    serv.calllog.delete(uid)
    return response_with(resp.SUCCESS_20000, value={"data": {}})


@view.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    serv.calllog.download(data)
    return response_with(resp.SUCCESS_20000, value={"data": {}})