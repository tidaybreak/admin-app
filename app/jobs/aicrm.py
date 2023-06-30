import os
import traceback
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from app.ext import celery, serv, influxdb
import time
import json, copy
import pytz
from influxdb import InfluxDBClient
from app.config import cfg
from app.utils.ciopaas.ciopaas import hm_data, call_ab_log, dial_task


def func_api(func):
    data = serv.dict.items_pages(typeCode='API')
    for ent in data['items']:
        try:
            val = ent['value'].split(',')
            url = val[0]
            api_access_id = val[1]
            api_access_secret = val[2]

            user = serv.user.find_by_username(username=ent['name'])
            if user is None:
                print("no link:", ent['name'])
                continue
            uid = user.id
            func(uid, url, api_access_id, api_access_secret)
        except Exception:
            traceback.print_exc()


def fun_report(uid, url, api_access_id, api_access_secret):
    start = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
    end = (datetime.now()).strftime("%Y-%m-%d 00:00:00")
    data = hm_data(url, api_access_id, api_access_secret,
                   start=start, end=end)
    print(len(data))
    for k, v in data.items():
        for k2, v2 in v.items():
            query_dict = {
                'date': k,
                'agent_name': k2
            }
            v2['__uid__'] = uid
            serv.report.update(query_dict, v2, insert=True)


def fun_calllog(uid, url, api_access_id, api_access_secret):
    data = call_ab_log(url, api_access_id, api_access_secret, days=7)
    print(len(data))
    for ent in data:
        ent['__uid__'] = uid
        #serv.calllog.update(query_dict, ent, insert=True)
        serv.calllog.insert(ent, action='add')


def fun_dailtask(uid, url, api_access_id, api_access_secret):
    data = dial_task(url, api_access_id, api_access_secret)
    print(len(data))
    for ent in data['data']['list']:
        query_dict = {
            'dial_task_main_sn': ent['dial_task_main_sn']
        }
        if uid:
            ent['__uid__'] = uid
        serv.bus_dialtask.update(query_dict, ent, insert=True)


@celery.task
def report_update(date=None):
    func_api(fun_report)
    return True, ''


@celery.task
def report_signature(args):
    return True, ""


@celery.task
def calllog_update(date=None):
    func_api(fun_calllog)
    return True, ''


@celery.task
def calllog_signature(args):
    return True, ""


@celery.task
def dialtask_update(date=None):
    func_api(fun_dailtask)
    return True, ''


@celery.task
def dialtask_signature(args):
    return True, ""


def crm_list_test(date=None, idc=[], action="grafana"):
    return {}
