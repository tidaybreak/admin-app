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
from app.utils.ciopaas.ciopaas import hm_data, call_ab_log


@celery.task
def report_update(date=None):
    data = serv.dict.items_pages(code='API')
    for ent in data['items']:
        val = ent['value'].split(',')
        url = val[0]
        api_access_id = val[1]
        api_access_secret = val[2]

        user = serv.user.find_by_username(username=ent['name'])
        if user is None:
            print("no link:", ent['name'])
            continue
        uid = user.id

        #api = serv.setting.config('api')
        print(val)
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
                v2['uid'] = uid
                serv.report.update(query_dict, v2, insert=True)
    return True, ''


@celery.task
def report_signature(args):
    return True, ""


@celery.task
def calllog_update(date=None):
    data = serv.dict.items_pages(code='API')
    for ent in data['items']:
        val = ent['value'].split(',')
        url = val[0]
        api_access_id = val[1]
        api_access_secret = val[2]

        user = serv.user.find_by_username(username=ent['name'])
        if user is None:
            print("no link:", ent['name'])
            continue
        uid = user.id

        #api = serv.setting.config('api')
        print(val)
        data = call_ab_log(url, api_access_id, api_access_secret, days=9)
        print(len(data))
        for ent in data:
            query_dict = {
                'sn': ent['sn']
            }
            ent['uid'] = uid
            #serv.calllog.update(query_dict, ent, insert=True)
            serv.calllog.insert(ent, action='add')
        #serv.calllog.bulk_save(data)

    return True, ''


@celery.task
def calllog_signature(args):
    return True, ""


def crm_list_test(date=None, idc=[], action="grafana"):
    return {}
