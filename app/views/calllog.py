# coding=utf-8


from app.ext import serv
from app.utils.responses import response_with
from app.utils import responses as resp
from app.utils.jwt import Jwt
from .base import *
from app.config import cfg
from app.utils.ciopaas.ciopaas import hm_data
from datetime import datetime, timedelta
import json

__author__ = 'Ti'


url_prefix = cfg.APP_BASE_API + "calllog"
view_name = os.path.basename(__file__).split('.')[0]
view = Blueprint(view_name, __name__)
view.before_request(Jwt.load_api)


@view.route('/pages', methods=['GET', 'POST'])
@view.route('/query', methods=['GET', 'POST'])
def query():

    # start = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
    # end = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d 23:59:59")
    # data = hm_data('ai193.ciopaas.com', 'be00bad65585da7e9202d30cef13a976', '61a460cb2640e62246bb92166d574804', start=start, end=end)
    # for k, v in data.items():
    #     for k2, v2 in v.items():
    #         query_dict = {
    #             'date': k,
    #             'agent_name': k2
    #         }
    #         serv.report.update(query_dict, v2, insert=True)
            #serv.report.update()

    #sess = Jwt.payload()
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


