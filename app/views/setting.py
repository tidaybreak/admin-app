from app.ext import serv
from app.utils.responses import response_with
from app.utils import responses as resp
from app.utils.jwt import Jwt
from .base import *
from app.config import cfg
import json

__author__ = "Ti"

url_prefix = cfg.APP_BASE_API + "setting"
view_name = os.path.basename(__file__).split('.')[0]
view = Blueprint(view_name, __name__)
view.before_request(Jwt.load_api)


@view.route("/query", methods=["GET"])
def query():
    result = serv.setting.query(None)

    return response_with(resp.SUCCESS_20000, value={"data": result})


@view.route("/update", methods=["POST"])
def update():
    body = request.json
    # config = body.get("config")
    reload_proc = body.get("reloadProc")
    records = []
    records.append({
        "query_dict": {"id": body['id']},
        "update_dict": {"id": body['id'], 'value': body['value']}
    })
    # for key, value in config.items():
    #     query_dict = {"key": key}
    #     if key.endswith("ENABLE"):
    #         value = str(value).lower()
    #     update_dict = {"value": value}
    #     records.append({
    #         "query_dict": query_dict,
    #         "update_dict": update_dict
    #     })

    ok, msg = serv.setting.update_record(records, reload_proc=reload_proc)
    return response_with(resp.SUCCESS_20000, value={"data": {}})