# coding=utf-8

from app.ext import serv, cache
from app.utils.responses import response_with
from app.utils import responses as resp
from app.utils.jwt import Jwt
from .base import *
from app.config import cfg
from app.utils.utils import view_cache_key

__author__ = 'Ti'

url_prefix = cfg.APP_BASE_API + "common"
view_name = os.path.basename(__file__).split('.')[0]
view = Blueprint(view_name, __name__)
view.before_request(Jwt.load_api)


@view.route("/select/get", methods=['GET', 'POST'])
#@cache.memoize(timeout=20, make_name=view_cache_key)
def select_get():
    query = request.get_json()
    #request.args.get('type')
    dtype = query['type']
    data = {}
    if dtype == 'username':
        data = serv.user.select_user()
    elif dtype == 'ciopass_user':
        uid = query['uid']
        data = serv.bus_dialtask.select_child_account(uid)

    return response_with(resp.SUCCESS_20000, value={"data": data})
