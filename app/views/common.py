# coding=utf-8

from urllib.parse import quote
import os
from ..ext import serv
from .base import *
from flask import session

__author__ = 'Ti'


url_prefix = "/api/v1/common"
view_name = os.path.basename(__file__).split('.')[0]
view = Blueprint(view_name, __name__)


@view.route("/download", methods=["GET", "POST"])
def download():
    file_name = request.values.get("file_name")
    if file_name == "":
        data = request.get_json()
        file_name = data.get("file_name", "")
    if not file_name:
        return res_json(code=500, message="文件不存在")
    file_path = "%s/%s" % (current_app.config["GLOBAL_TEMP_PATH"], file_name)
    rv = send_file(file_path, as_attachment=True, attachment_filename=quote(file_name))
    rv.headers['Content-Disposition'] = "attachment; filename*={utf_filename}".format(utf_filename=quote(file_name))
    return rv


@view.route("/job/result/get.json", methods=["GET", "POST"])
def get_job_result():
    task_id = request.values.get("task_id")
    result = serv.celery.AsyncResult(task_id).result
    success = False
    if isinstance(result, list):
        return res_json(
            code=200,
            data=result[0],
            message=result[1],
            success=True
        )
    elif isinstance(result, dict):
        return res_json(
            code=200,
            data=result,
            message="未完成",
            success=False
        )
    else:
        return res_json(
            code=200,
            data=success,
            message="未完成",
            success=False
        )


@view.route("/test.json", methods=["GET", "POST"])
def test():
    return res_json(
        code=200,
        message="",
        data={}
    )
