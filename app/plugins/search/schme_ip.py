# coding:utf-8

__author__ = 'ti'

import re
from IPy import IP
from app.utils.utils import export


@export("Schema_ip")
def schema_ip(body, *args, **kwargs):
    if "q" in body:
        # IP按掩码查询
        if body["q"].find("/") >= 0:
            q = body["q"]
            # 把不是网络号的IP段，统一转化为网络号
            attr_last = q.split(".")
            attr_ip_last = attr_last[3].split("/")
            ip_bit = 2 ** (32 - int(attr_ip_last[1]))
            ip_nu = int(attr_ip_last[0]) // ip_bit
            ip_network = ip_nu * ip_bit
            attr1 = re.sub(r'\d+/', str(ip_network) + '/', q)
            iplist = []
            ips = IP(attr1)
            for i in ips:
                ip = str(i)
                iplist.append(ip)

            if iplist:
                body["q"] = "*"
                # 移除init加的模糊查询
                for must in body["filter"]["bool"]["must"]:
                    if "match" in must:
                        body["filter"]["bool"]["must"].remove(must)
                body["filter"]["bool"]["must"].append({"terms": {"ip": iplist}})
        else:
            # 搜ip字段
            f_ip = re.findall(r'^(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.)+', body["q"])
            if f_ip:
                # 移除init加的模糊查询
                for must in body["filter"]["bool"]["must"]:
                    if "match" in must:
                        body["filter"]["bool"]["must"].remove(must)
                # body["filter"]["bool"]["must"] = [{"match": {"ip": body["q"]}}]
                body["filter"]["bool"]["must"].append({"match": {"ip": body["q"]}}) # 201214.不能进行覆盖，因为传递过来还有其他的参数

    # 没有排序则默认给一个
    find_ip_sort_key = False
    if body.get("sort"):
        for item in body["sort"]:
            for key, value in list(item.items()):
                if key == "ip":
                    find_ip_sort_key = True
                    break
    if not find_ip_sort_key:
        ip_sort = [{
            "ip": {
                "order": "asc",
                "missing": "_last",
                "ignore_unmapped": True,
                "type": "IP"
            }
        }]
        if not body["sort"]:
            body["sort"] = []
        body["sort"] = body["sort"] + ip_sort

    return body
