import os
import traceback
from urllib.parse import quote

from flask import Blueprint, current_app, request, make_response, send_file
from app.utils.utils import res_json, isNone
from app.ext import celery

__author__ = "Ti"


def curd_create(service):
    pass


def curd_list(service):
    try:
        body = request.json
        page = body.get("page", 1)
        limit = body.get("limit", 10)
        query_dict = body.get("query_dict", {})
        result = service.fetch_list(page=page, limit=limit, query_dict=query_dict)
        return res_json(code=200, data=result)
    except Exception as e:
        traceback.print_exc()
        return res_json(code=500, message="解析post数据错误：%s" % str(e))


def curd_update(service):
    try:
        body = request.json
        ok, msg = service.bulk_update([body])
        return res_json(code=200 if ok else 500, message=msg)
    except Exception as e:
        traceback.print_exc()
        return res_json(code=500, message=str(e))


def curd_delete(service):
    pass


def aync_job_query():
    params = request.values
    task_id = params.get("task_id")
    if not task_id:
        return res_json(
            code=500,
            data=False,
            message="缺少参数task_id",
            success=False
        )
    task = celery.AsyncResult(task_id)
    state = task.state
    result = task.result
    if state == "PENDING":
        return res_json(
            code=200,
            data=False,
            message="任务尚未开始",
            success=False
        )
    if state == "FAILURE":
        return res_json(
            code=500,
            data=False,
            message="产生了意料之外的错误 %s" % str(result.info),
            success=False
        )
    if state == "REVOKED":
        return res_json(
            code=500,
            data=False,
            message="任务已撤销",
            success=False
        )
    if state == "RETRY":
        return res_json(
            code=200,
            data=False,
            message="任务正在重试",
            success=False
        )
    if state == "STARTED":
        return res_json(
            code=200,
            data=False,
            message="任务处理中",
            success=False
        )

    if not result[0]:
        return res_json(
            code=500,
            data=False,
            message="错误 %s" % str(result[1]),
            success=False
        )
    return res_json(
        code=200,
        data=result[1],
        message="",
        success=True
    )

def async_download():
    params = request.values
    task_id = params.get("task_id")
    fname = params.get("file_name")
    if not (task_id and fname):
        return res_json(
            code=500,
            data=False,
            message="缺少参数task_id或file_name",
            success=False
        )
    task = celery.AsyncResult(task_id)
    state = task.state
    if state != "SUCCESS":
        return res_json(
            code=500,
            data=False,
            message="任务不存在或未完成",
            success=False
        )
    result = task.result

    if not result[0]:
        return res_json(
            code=200,
            data=False,
            message="错误 %s" % result[1],
            success=False
        )

    if result[1] != fname:
        return res_json(
            code=200,
            data=False,
            message="task_id与文件名不符",
            success=False
        )

    full_fpath = os.path.join(current_app.config["GLOBAL_TEMP_PATH"], fname)
    stream = None
    with open(full_fpath, "rb") as f:
        stream = f.read()
    # 删除文件
    os.remove(full_fpath)
    resp = make_response(stream)
    filename = fname.split("!")[1]
    filename = quote(filename)
    resp.headers["Content-Disposition"] = "attachment; filename=%s" % (filename, )
    resp.headers["Content-Type"] = "application/octet-stream"
    return resp
