# coding=utf-8


from app.ext import serv
from app.utils.responses import response_with
from app.utils import responses as resp
from app.utils.jwt import Jwt
from .base import *
from app.config import cfg
import json

__author__ = 'Ti'


url_prefix = cfg.APP_BASE_API + "permissions"
view_name = os.path.basename(__file__).split('.')[0]
view = Blueprint(view_name, __name__)
view.before_request(Jwt.load_api)


@view.route('/list', methods=['GET'])
def permissions():
    result = [
            {
                "id": 1,
                "name": "权限1",
                "checked": 1
            },
            {
                "id": 2,
                "name": "权限2",
                "checked": 1
            },
            {
                "id": 3,
                "name": "权限3",
                "checked": 1
            }
        ]
    return response_with(resp.SUCCESS_20000, value={"data": result})

