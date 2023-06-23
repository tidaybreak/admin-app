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
    print("login:", response.json())
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
    print("session:", session)
    data.update(session)

    url = 'https://'+host+'/api/crmList'
    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()
    if "data" not in result:
        login(host, api_access_id, api_access_secret)
        print(session)
        data.update(session)
        response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


def crm_list_all(host, api_access_id, api_access_secret,
                 start=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d 00:00:00"),
                 end=(datetime.now()).strftime("%Y-%m-%d 00:00:00")):
    page = 0
    pageIndex = 5000
    data = crm_list(host, api_access_id, api_access_secret, pageIndex=page, pageSize=pageIndex,
                    start=start,
                    end=end)
    if "data" not in data:
        print("接口错误：", data)
        return []
    result = data["data"]["list"]
    total = data["data"]["total"]
    print(total, page)
    total -= len(data["data"]["list"])
    while total > 0:
        page += 1
        data2 = crm_list(host, api_access_id, api_access_secret, pageIndex=page, pageSize=pageIndex,
                         start=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d 00:00:00"),
                         end=(datetime.now()).strftime("%Y-%m-%d 00:00:00"))
        if "data" not in data2:
            print("接口错误：", data2)
            return []
        if len(data2["data"]["list"]) == 0:
            print(data2)
            break
        total -= len(data2["data"]["list"])
        print(total, page)
        result += data2["data"]["list"]

    #print(len(result))
    return result


def check_add(data, key):
    if key not in data or data[key] is None:
        return 0
    if isinstance(data[key], int) and data[key] > 0:
        return 1
    if isinstance(data[key], str) and data[key] != "":
        return 1
    return 0


def rate(val1, val2):
    if val2 > 0:
        return round(val1 / val2, 2)
    return 0.0


def hm_data(host, api_access_id, api_access_secret, start, end):
    data = crm_list_all(host, api_access_id, api_access_secret, start, end)
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
                'connection_count': 0,       # 接通数量

                #'fs_listen_agent': 0,                   # 监听坐席
                #'fs_monitor_change_talk': 0,            # 是否介入
                #'fs_push_screens': 0,                   # 是否弹屏
                #'fs_intervention_time': 0,              # 介入时长

                'pushed_at': 0,                         # 弹屏时间
                'listened_at': 0,                       # 监听时间
                'intervention_at': 0,                   # 介入时间
                'pushed_rate': 0,                         # 弹屏率
                'listened_rate': 0,                       # 监听率
                'intervention_rate': 0,                   # 介入率

                #'fs_push_screens_total': 0,             # 发起弹屏坐席个数
                #'actual_push_screens_total': 0,         # 实际弹屏坐席个数
            }

        date_hm[day][hm]['outbound_count'] += 1
        date_hm[day][hm]['connection_count'] += check_add(ent, 'talktimes')

        #date_hm[day][hm]['fs_listen_agent'] += check_add(ent, 'fs_listen_agent')
        #date_hm[day][hm]['fs_monitor_change_talk'] += check_add(ent, 'fs_monitor_change_talk')
        #date_hm[day][hm]['fs_push_screens'] += check_add(ent, 'fs_push_screens')
        #date_hm[day][hm]['fs_intervention_time'] += check_add(ent, 'fs_intervention_time')
        date_hm[day][hm]['pushed_at'] += check_add(ent, 'pushed_at')
        date_hm[day][hm]['listened_at'] += check_add(ent, 'listened_at')
        date_hm[day][hm]['intervention_at'] += check_add(ent, 'intervention_at')
        #date_hm[day][hm]['fs_push_screens_total'] += check_add(ent, 'fs_push_screens_total')
        #date_hm[day][hm]['actual_push_screens_total'] += check_add(ent, 'actual_push_screens_total')

    for k, v in date_hm.items():
        for k2, v2 in v.items():
            date_hm[k][k2]['connection_rate'] = rate(v2['connection_count'], v2['outbound_count'])  # 接通率

            date_hm[k][k2]['pushed_rate'] = rate(v2['pushed_at'], v2['connection_count'])
            date_hm[k][k2]['listened_rate'] = rate(v2['listened_at'], v2['pushed_at'])
            date_hm[k][k2]['intervention_rate'] = rate(v2['intervention_at'], v2['listened_at'])

    print(date_hm)
    return date_hm

