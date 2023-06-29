# coding=utf-8

import os
from app.ext import serv
from app.utils.utils import res_json
from celery import chain
from app.utils.responses import response_with
from app.jobs.aicrm import report_update, calllog_update
from app.utils.ciopaas.ciopaas import call_ab_log, aiUserDatasapi
from app.utils import responses as resp
from app.utils.jwt import Jwt
from flask import Blueprint, current_app, request, session
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


@view.route("/test")
def test():

    #return response_with(resp.SUCCESS_20000, value={"data": calllog_update()})

    host = 'ai193.ciopaas.com'
    api_access_id = 'be00bad65585da7e9202d30cef13a976'
    api_access_secret = '61a460cb2640e62246bb92166d574804'
    #data = call_ab_log(host, api_access_id, api_access_secret, days=12)
    data = aiUserDatasapi(host, api_access_id, api_access_secret)
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route(cfg.APP_BASE_API + "/captcha")
def captcha():
    data = {
        "verifyCodeKey": "a13edfb639ef4fc5b3ee8526b6a42dcb",
        "verifyCodeImg": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAAkCAIAAADNSmkJAAAEU0lEQVR42u2Zb0hbVxjG3bqyD91GC5bRsn8f9mmwQSn0m4PtQ8sYYwNhMMY+DIasira01jS2QlFaZVvZujGZUSNbNBJtdWvaoqV/tLGtqU1rqFa002DX6Oq/VFvXGJI8e87C1uSabd6bm1wK5+EQ7nnvId77y8tz3veYBamMKEsikKAl6BQUieD8eRw8CLNZfDqdmJ+XoNOgjg7B99YtzMxgdBQOB0wmTE5K0HqruBj9/QmRkydRWytB6628PIRCCRGmNm1EgtZZO3dicTEh4vHgyBEJWm9VV6On59E0GMSBA4K1BJ2gLp+v7Ny5XIfjPbv9w9bWiu7uq36/qm/gBsikpi8TMbfEigo0N8uqI07+hYVP2to+Onr056EhXyDAqWt8vP7aNRIvPHUq8PDhyv8kN0PypVnzs7dX1tFxuj0//05jo2NgYPmtxVCIec0cV8VaNizLFFqIus3+uo0Ry2o0PIfjb2LUkcR5+/qY15l43kAALS0oL8eOHcjPx759sNkwPW0IO88ktnfg9To8exjPHMbbdnSNawMdnEPLa6jJUo4rpYqF4Ujkg+ZmtX6tWmNjKCwUpqMYRUXw+QxI0krlWFWFzjENoC8WEets3XrPpWoBncPXhsYXYHkSM/2KtfYbN+gh6X2zqiqBtbISIyOgU3EMD4tGk0Heyrg2WfG9B757WApjYFpkNFlvbtAAuulFgi6qK/l1djZuWzwrkrp3j2It17AOUZULqkWvIFN2OIqGh8GCAsNd2H9fvNTTX2gAXbuaTHNqvlW4tgD9S45i7d0HD7hhphd0aem/gt6/33DQTGq+1MvVGkDbNpBpQe2epXBYmdG2jYq17jt3WHukFzStSWEdvDh0SARdLmMpD07j1R/ES1Vd1gC6+7OYR49crf/bo9vR9JIAXb9G+aN4vexl0gta/J5u0UrG74Sc9vWlvo8lHSvUlQms/Vqsf7cF4agG0IsTMZtOGBfyxKdllaLqoEF3rXjr1w76zBns2pUAmlMGjQM9FkD2N2JxbhuCYc119B+/h135dy3ZUctTsL8C75eYGxCgG9bGr/rO7WbfmOKL/b96egTZvXtx/bo4muLgBacMxh+gZFbky4f/+Dgi0ZQ7w8Gpqa0227GbN8VkxCZAt77xz1025dwG2ZSnHXTMNFjSxYvTmIEYpHV/mcbEfZ3OOsiaNNn+TbVvE6Bdn7P5plfkOZ00jdsq/x+VUnkXDCZ2VUEN5Z2O1hFbGdXx9I61R+elpmjNEwT9aY0px2rdfuKEc3iYBq3NIlVr9+4kGT00JILFxcaCTvmsw/kWfutAcBZL94Rp/Jgt0vl0ri7Nq2pZrYKp2Qyv95FHm0wiyFuP96HS8oOO9i0CuiGg2aCWlCQ562Bwbs4wgvpk9OQFdL6Pn54XhfOxTfB+hchSxh4uibjlsi0qKxN+zcELTv9zH35MQEtlyDqkJGgJWkqClqAlaCkJWoKWWq4/AYzDjqehSyo4AAAAAElFTkSuQmCC"
    },
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route(cfg.APP_BASE_API + '/users/login', methods=['POST'])
@view.route(cfg.APP_BASE_API + '/oauth/token', methods=['POST'])
def token():
    data = request.get_json()
    result = serv.user.get_token(data)
    if session.get('userinfo'):
        return response_with(resp.SUCCESS_20000, value=result)
    else:
        return response_with(resp.UNAUTHORIZED_401, value=result)


@view.route(cfg.APP_BASE_API + '/oauth/logout', methods=['POST', 'DELETE'])
def authenticate_logout():
    return response_with(resp.SUCCESS_20000, value={"data": {}})


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
