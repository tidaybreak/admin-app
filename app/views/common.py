# coding=utf-8

from app.ext import serv, cache
from app.utils.responses import response_with
from app.utils import responses as resp
from app.utils.jwt import Jwt
from .base import *
import uuid
import tempfile
from app.config import cfg

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
    elif dtype == 'templatelist':
        uid = query['uid']
        data = serv.bus_dialtask.select_templatelist(uid)
    return response_with(resp.SUCCESS_20000, value={"data": data})


@view.route("/upload", methods=['POST'])
def upload():
    data = {}
    if 'file' in request.files:
        operate = request.values.get("operate")

        # 开始解析xls文件
        f = request.files['file']
        ext = f.filename.split('.')[-1]
        if ext not in ["csv", "xls", "xlsx"]:
            raise ValueError("文件扩展名必须为.csv .xls或者.xlsx的文件")

        file_name = "%s.%s" % (uuid.uuid4().hex, ext)
        temp = tempfile.TemporaryFile()
        file_path = os.path.join(current_app.config["GLOBAL_TEMP_PATH"], file_name)
        f.save(file_path)
        temp.close()
        data['file_name'] = file_name
    return response_with(resp.SUCCESS_20000, value={"data": data})
