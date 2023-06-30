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

    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
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
             end=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d 00:00:00"),
             status=''):
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
    if status != '':
        data['status'] = status
    print("session:", session)
    data.update(session)

    url = 'https://'+host+'/api/crmList'
    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
    result = response.json()
    if "data" not in result:
        login(host, api_access_id, api_access_secret)
        print(session)
        data.update(session)
        response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


# 子账号列表 http://wiki.ciopaas.com:8888/web/#/4?page_id=31
def aiUserDatasapi(host, api_access_id, api_access_secret):
    current_timestamp = int(time.time())
    if current_timestamp > session["api_key_expire"] - 60:
        login(host, api_access_id, api_access_secret)

    headers = {'Content-Type': 'application/json'}

    data = {
        "pageIndex": "0",
        "pageSize": "1000"
    }

    print("session:", session)
    data.update(session)

    url = 'https://'+host+'/api/aiUserDatasapi'
    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()
    if "data" not in result:
        login(host, api_access_id, api_access_secret)
        print(session)
        data.update(session)
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
    # {
    #     callin_project_sn: "projects|eea500f6b57ba70ebe55cca2fc341581",
    #     contact: "梁秋平",
    #     display_phone: "",
    #     expired: null,
    #     ext: "1",
    #     job: "坐席",
    #     last_login_time: "2023-06-16 08:49:01",
    #     linkext: "1",
    #     max_call_count: 15,
    #     organization_id: 216,
    #     parent_sn: "mo912143",
    #     project_sn: "projects|eea500f6b57ba70ebe55cca2fc341581",
    #     sdzj_phone: "912143",
    #     sipname: "mo912143002",
    #     skillgroup_sn: "mo912143002",
    #     user_name: "mo912143002",
    #     user_sn: "SYSUSER|cfc70685b3a4f159b4b8d44e59af68b8",
    #     wangwang: null,
    #     yd_display_phone: "vos:912143"
    # }
    return response.json()


# 任务管理列表 http://wiki.ciopaas.com:8888/web/#/4?page_id=52
def dial_task(host, api_access_id, api_access_secret):
    current_timestamp = int(time.time())
    if current_timestamp > session["api_key_expire"] - 60:
        login(host, api_access_id, api_access_secret)

    headers = {'Content-Type': 'application/json'}

    data = {
        "pageIndex": "0",
        "pageSize": "99999"
        #"api_key": "TEcAVs9a",
        #"user_sn": "SYSUSER|cb31d43bc89487492bb0e0dd720705e0",
        #"start_create_at": "2019-01-22",
        #"end_create_at": "2019-01-22"
    }

    print("session:", session)
    data.update(session)

    url = 'https://'+host+'/api/index'
    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
    result = response.json()
    if "data" not in result:
        login(host, api_access_id, api_access_secret)
        print(session)
        data.update(session)
        response = requests.post(url, headers=headers, data=json.dumps(data))
        # {
        #     "dial_task_main_id":1826,
        #     "dial_task_main_sn":"dial_task_main_sn|e69342205b8bca83b06401a7705f4b7c",
        #     "status":"发送中",
        #     "user_sn":"SYSUSER|cdbe0021b3f5e11f43c9175757b11e2e",
        #     "user_name":"hln2",
        #     "team_sn":"ROOT|0008",
        #     "team_name":"测试",
        #     "created_at":"2018-05-08 15:40:10",
        #     "last_modify":"2018-05-08 15:40:10",
        #     "started_at":"2018-05-08 15:40:10",
        #     "stoped_at":"2018-05-08 15:41:44",
        #     "total_count":3,
        #     "send_count":2,
        #     "remark":null,
        #     "ring_groups":null,
        #     "priority":null,
        #     "project_sn":"",
        #     "percentage":null,
        #     "source":"测试",
        #     "batch":"hln20180508154010",
        #     "trunkgroup_sn":null,
        #     "caller_group":null,
        #     "mark":null,
        #     "operator":"hln",
        #     "project_caption":"测试",
        #     "parent_sn":"hln",
        #     "success":"1",
        #     "fail":"1",
        #     "stops":"0",
        #     "unsend_count":1,
        #     "percent":"50%"
        # }
    return response.json()


def crm_list_all(host, api_access_id, api_access_secret,
                 start=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d 00:00:00"),
                 end=(datetime.now()).strftime("%Y-%m-%d 00:00:00"),
                 status=''):
    page = 0
    pageIndex = 5000
    data = crm_list(host, api_access_id, api_access_secret, pageIndex=page, pageSize=pageIndex,
                    start=start,
                    end=end,
                    status=status)
    if "data" not in data:
        print("接口错误：", data)
        return []
    result = data["data"]["list"]
    total = data["data"]["total"]
    print("total:", total, page)
    total -= len(data["data"]["list"])
    print("remaining:", total, page)
    while total > 0:
        page += 1
        data2 = crm_list(host, api_access_id, api_access_secret, pageIndex=page, pageSize=pageIndex,
                         start=start,
                         end=end)
        if "data" not in data2:
            print("接口错误：", data2)
            return []
        if len(data2["data"]["list"]) == 0:
            print(data2)
            break
        total -= len(data2["data"]["list"])
        print("remaining:", total, page)
        result += data2["data"]["list"]

    #print(len(result))
    return result


def check_add(data, key, log=False):
    if key not in data or data[key] is None:
        return 0
    if isinstance(data[key], int) and data[key] > 0:
        if log:
            print(key, data[key])
        return 1
    if isinstance(data[key], str) and data[key] != "":
        if log:
            print(key, data[key])
        return 1
    return 0


def rate(val1, val2):
    if val2 > 0:
        return round(val1 / val2, 2)
    return 0.0


def hm_data(host, api_access_id, api_access_secret, start, end):
    data = crm_list_all(host, api_access_id, api_access_secret, start, end)
    date_hm = dict()
    count = dict()
    for ent in data:
        day = ent["created_at"][:10]
        if day not in date_hm:
            date_hm[day] = dict()
            count[day] = 0

        hm = ent["user_name"]
        if hm not in date_hm[day]:
            date_hm[day][hm] = {
                'agent_name': ent['user_name'],
                'company_name': ent['parent_sn'],
                'outbound_area': '',             # 外呼地区
                'outbound_count': 0,        # 外呼数量
                'connection_count': 0,      # 接通数量
                'connection_rate': 0,       # 接通率

                #'fs_listen_agent': 0,                   # 监听坐席
                #'fs_monitor_change_talk': 0,            # 是否介入
                #'fs_push_screens': 0,                   # 是否弹屏
                #'fs_intervention_time': 0,              # 介入时长

                'screen_pop_count': 0,                  # 可弹屏数
                'screen_pop_rate': 0,                   # 可弹屏率
                'offline_screen_pop_count': 0,          # 未在线弹屏
                'offline_screen_pop_rate': 0,           # 未在线弹屏率

                'pushed_at': 0,                         # 弹屏时间
                'listened_at': 0,                       # 监听时间
                'intervention_at': 0,                   # 介入时间
                'pushed_rate': 0,                         # 弹屏率
                'listened_rate': 0,                       # 监听率
                'intervention_rate': 0,                   # 介入率

                'customer_count': 0,                      # 客户数量
                'connected_customer_success_rate': 0,     # 接通客户成功率
                'intervention_customer_success_rate': 0,  # 介入客户成功率

                #'fs_push_screens_total': 0,             # 发起弹屏坐席个数
                #'actual_push_screens_total': 0,         # 实际弹屏坐席个数
            }

        count[day] += 1

        date_hm[day][hm]['outbound_count'] += 1
        date_hm[day][hm]['connection_count'] += check_add(ent, 'talktimes')

        #date_hm[day][hm]['fs_listen_agent'] += check_add(ent, 'fs_listen_agent')
        #date_hm[day][hm]['fs_monitor_change_talk'] += check_add(ent, 'fs_monitor_change_talk')
        #date_hm[day][hm]['fs_push_screens'] += check_add(ent, 'fs_push_screens')
        #date_hm[day][hm]['fs_intervention_time'] += check_add(ent, 'fs_intervention_time')

        # 0623 实际6个 有一个fs_push_screens是2不计
        if ent['fs_push_screens'] == 1:
            date_hm[day][hm]['pushed_at'] += 1
            date_hm[day][hm]['screen_pop_count'] += 1
        elif ent['fs_push_screens'] == 2:
            date_hm[day][hm]['offline_screen_pop_count'] += 1
            date_hm[day][hm]['screen_pop_count'] += 1
        date_hm[day][hm]['listened_at'] += check_add(ent, 'listened_at')
        date_hm[day][hm]['intervention_at'] += check_add(ent, 'intervention_at')

        #date_hm[day][hm]['fs_push_screens_total'] += check_add(ent, 'fs_push_screens_total')
        #date_hm[day][hm]['actual_push_screens_total'] += check_add(ent, 'actual_push_screens_total')

        if 'status_manual' in ent and isinstance(ent['status_manual'], str) and (ent['status_manual'].find('A') >= 0 or ent['status_manual'].find('B') >= 0):
            date_hm[day][hm]['customer_count'] += 1

    for k, v in date_hm.items():
        for k2, v2 in v.items():
            date_hm[k][k2]['connection_rate'] = rate(v2['connection_count'], v2['outbound_count'])  # 接通率

            date_hm[k][k2]['screen_pop_rate'] = rate(v2['screen_pop_count'], v2['outbound_count'])
            date_hm[k][k2]['offline_screen_pop_rate'] = rate(v2['offline_screen_pop_count'], v2['connection_count'])

            date_hm[k][k2]['pushed_rate'] = rate(v2['pushed_at'], v2['connection_count'])
            date_hm[k][k2]['listened_rate'] = rate(v2['listened_at'], v2['pushed_at'])
            date_hm[k][k2]['intervention_rate'] = rate(v2['intervention_at'], v2['listened_at'])

            date_hm[k][k2]['connected_customer_success_rate'] = rate(v2['customer_count'], v2['connection_count'])
            date_hm[k][k2]['intervention_customer_success_rate'] = rate(v2['customer_count'], v2['intervention_at'])

    print(start, end, count)
    print(date_hm)
    return date_hm


def call_ab_log(host, api_access_id, api_access_secret, days=7):
    start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d 00:00:00")
    end = (datetime.now()).strftime("%Y-%m-%d 00:00:00")
    data = crm_list_all(host, api_access_id, api_access_secret, start, end, status='A,B')
    date_hm = dict()
    count = dict()
    return data
    for ent in data:
        day = ent["created_at"][:10]


def get_user_list(api):
    val = api['value'].split(',')
    host = val[0]
    api_access_id = val[1]
    api_access_secret = val[2]
    return aiUserDatasapi(host, api_access_id, api_access_secret)