# coding=utf-8


from app.ext import serv
from app.utils.responses import response_with
from app.utils import responses as resp
from app.utils.jwt import Jwt
from .base import *
from app.config import cfg
import json

__author__ = 'Ti'


url_prefix = cfg.APP_BASE_API + "user"
view_name = os.path.basename(__file__).split('.')[0]
view = Blueprint(view_name, __name__)
view.before_request(Jwt.load_api)


@view.route('/info', methods=['GET'])
def authenticate_info():
    userinfo = Jwt.payload()
    result = serv.user.get_info(userinfo['username'])
    return response_with(resp.SUCCESS_20000, value={"data": result})


@view.route('/logout', methods=['POST'])
def authenticate_logout():
    return response_with(resp.SUCCESS_20000, value={"data": {}})
