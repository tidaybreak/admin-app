from datetime import datetime

from app.utils.utils import res_json
from app.ext import serv
from .base import *

from flask import request, current_app

__author__ = "Ti"

url_prefix = "/api/v1/config"
view_name = os.path.basename(__file__).split('.')[0]
view = Blueprint(view_name, __name__)

@view.route("/list", methods=["GET"])
def fetch_list():
    params = request.values
    section = params.get("section", "")
    prefix = params.get("prefix", "")
    data = serv.config.fetch_list(section, prefix)
    return res_json(
        code=200,
        data=data,
        message="",
        success=True
    )

@view.route("/update", methods=["POST"])
def update():
    body = request.json
    config = body.get("config")
    reload_proc = body.get("reloadProc")
    records = []
    for key, value in config.items():
        query_dict = {"key": key}
        if key.endswith("ENABLE"):
            value = str(value).lower()
        update_dict = {"value": value}
        records.append({
            "query_dict": query_dict,
            "update_dict": update_dict
        })

    ok, msg = serv.config.update_record(records, reload_proc=reload_proc)
    return res_json(
        code=200 if ok else 500,
        data=ok,
        message=msg,
        success=ok
    )