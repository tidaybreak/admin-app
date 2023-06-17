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
from app.utils.ciopaas.ciopaas import hm_data


@celery.task
def crm_list(date=None):
    data = hm_data('ai193.ciopaas.com', 'be00bad65585da7e9202d30cef13a976', '61a460cb2640e62246bb92166d574804')
    print(len(data))
    for k, v in data.items():
        for k2, v2 in v.items():
            query_dict = {
                'date': k,
                'agent_name': k2
            }
            serv.report.update(query_dict, v2, insert=True)
    return True, ''


@celery.task
def crm_list_signature(args):
    return True, ""


def crm_list_test(date=None, idc=[], action="grafana"):
    return {}
