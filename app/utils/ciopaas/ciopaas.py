import requests
import json
from datetime import datetime, timedelta
import hashlib
import time

session = {
    "user_sn": "",
    "api_key": "",
    "api_key_expire": 0
}


def login(host, api_access_id, api_access_secret):
    global session
    # url = 'https://ai193.ciopaas.com/api/login'
    # be00bad65585da7e9202d30cef13a976
    # 61a460cb2640e62246bb92166d574804
    url = 'https://'+host+'/api/login'
    headers = {'Content-Type': 'application/json'}
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sign = hashlib.md5((api_access_id + api_access_secret + timestamp).encode()).hexdigest()

    data = {
        "api_access_id": api_access_id,
        "from": 1,
        "sign": sign,
        "timestamp": timestamp
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    # {
    #     "code": 0,
    #     "data": {
    #         "id": 2436,
    #         "user_name": "mo912143",
    #         "user_sn": "SYSUSER|ab546199538df684ced4ac763749b9a7",
    #         "team_name": "周翠翠客户",
    #         "expired": "2023-07-11",
    #         "ai_count": 15,
    #         "caller_group": "912143",
    #         "api_key": "1zjsyRCx",
    #         "parent_sn": null,
    #         "status": null,
    #         "api_key_expire": 1686824884,
    #         "team_sn": "SON|8156510022",
    #         "job": "管理员"
    #     },
    #     "msg": "login success"
    # }
    data = response.json()
    if data["code"] == 0:
        session = {
            "user_sn": data["data"]["user_sn"],
            "api_key": data["data"]["api_key"],
            "api_key_expire": data["data"]["api_key_expire"]
        }
    return response.json()


# 获取流水列表接口 http://wiki.ciopaas.com:8888/web/#/4?page_id=54
def crm_list(host, api_access_id, api_access_secret,
             pageIndex=0,
             pageSize=10000,
             start=datetime.now().strftime("%Y-%m-%d 00:00:00"),
             end=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")):
    current_timestamp = int(time.time())
    if current_timestamp > session["api_key_expire"] - 60:
        login(host, api_access_id, api_access_secret)

    headers = {'Content-Type': 'application/json'}

    data = {
        "pageIndex": pageIndex,
        "pageSize": pageSize,
        "start_create_at": start,
        "end_create_at": end,
        "dial_task_main_sn": "",
        "ids_json": "",
        "project_sn": "",
        "namephone": "",
        "talktimes_min": "",
        "talktimes_max": "",
        "turn_count_min": "",
        "turn_count_max": "",
        "hangup_serial_number": "",
        "qc_status": "",
        "return_visit": "",
        "score_min": "",
        "score_max": "",
        "asks_count_min": "",
        "asks_count_max": "",
        "area_code": "",
        "fs_intervention_time_min": "",
        "fs_intervention_time_max": "",
        "seating_assistance": "",
        "warning_times_min": "",
        "warning_times_max": "",
        "warning_results": "",
        "dynamic_labelling": "",
        "mark": "",
        "status_search": "status"
    }
    print(session)
    data.update(session)

    url = 'https://'+host+'/api/crmList'
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


def crm_list_all(host, api_access_id, api_access_secret):
    page = 0
    pageIndex = 5000
    data = crm_list(host, api_access_id, api_access_secret, pageIndex=page, pageSize=pageIndex,
                    start=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d 00:00:00"),
                    end=(datetime.now()).strftime("%Y-%m-%d 00:00:00"))
    result = data["data"]["list"]
    total = data["data"]["total"]
    print(total, page)
    total -= len(data["data"]["list"])
    while total > 0:
        page += 1
        data2 = crm_list(host, api_access_id, api_access_secret, pageIndex=page, pageSize=pageIndex,
                         start=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d 00:00:00"),
                         end=(datetime.now()).strftime("%Y-%m-%d 00:00:00"))
        if len(data2["data"]["list"]) == 0:
            print(data2)
            break
        total -= len(data2["data"]["list"])
        print(total, page)
        result += data2["data"]["list"]

    #print(len(result))
    return result


def hm_data(host, api_access_id, api_access_secret):
    data = crm_list_all(host, api_access_id, api_access_secret)
    date_hm = dict()
    for ent in data:
        day = ent["created_at"][:10]
        if day not in date_hm:
            date_hm[day] = dict()

        hm = ent["user_name"]
        if hm not in date_hm[day]:
            date_hm[day][hm] = {
                'agent_name': ent['user_name'],
                'company_name': ent['parent_sn'],
                'outbound_area': '',             # 外呼地区
                'outbound_count': 0,        # 外呼数量
                'connection_count': 0       # 接通数量
            }

        date_hm[day][hm]['outbound_count'] += 1
        if ent['talktimes'] > 0:
            date_hm[day][hm]['connection_count'] += 1

    for k, v in date_hm.items():
        for k2, v2 in v.items():
            date_hm[k][k2]['connection_rate'] = round(v2['connection_count'] / v2['outbound_count'], 2)  # 接通率
    return date_hm

