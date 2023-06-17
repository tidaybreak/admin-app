# coding:utf-8

__author__ = 'ti'

from app.utils.utils import export
from app.ext import serv, cache
from app.utils.utils import parse_q


@export("Init")
def body_init(schema, body, *args, **kwargs):
    # attrs to filter
    if "filter" not in body or not body["filter"]:
        body["filter"] = {}
    if "bool" not in body["filter"] or not body["filter"]["bool"]:
        body["filter"]["bool"] = {}
    if "must" not in body["filter"]["bool"] or not body["filter"]["bool"]["must"]:
        body["filter"]["bool"]["must"] = []
    if "should" not in body["filter"]["bool"] or not body["filter"]["bool"]["should"]:
        body["filter"]["bool"]["should"] = []

    if "attrs" in body and body["attrs"]:
        for key, value in list(body["attrs"].items()):
            # 可能传*
            if value != "*":
                if value.startswith("*"):
                    value = value.replace("*", "")
                    body["filter"]["bool"]["must"].append({"match": {key: value}})
                elif " OR " in value:
                    # 支持对特定字段的多值查询
                    value_list = value.split(" OR ")
                    body["filter"]["bool"]["must"].append({"match": {key: value_list}})
                else:
                    body["filter"]["bool"]["must"].append({"terms": {key: [value]}})

        body["attrs"] = {}

    # 查找key
    if "q" in body and body["q"].startswith("N_"):
        body["q"] = "entity.key:%s" % body["q"]

    if body.get("q", "*") != "*":
        # k1:v1 or k2:v2 or v3
        with_wild = body["with_wild"]
        psql = parse_q(body.get("q"))
        if psql and isinstance(psql, (tuple, list)):
            bool_type = psql[0]
            list_attrs = psql[1]
            dict_attrs = psql[2]
            sub_query = []
            for attr in list_attrs:
                match = with_wild
                if attr.endswith("$") and attr.startswith("^"):
                    attr = attr[1:-1]
                    match = False

                if match:
                    sub_query.append({"match": {"attributes.*": attr}})
                else:
                    # TODO 全字段匹配比模糊更慢，考虑用 func.JSON_EXTRACT(models.Entity.attributes, "$.*").like('%%"%s"%%' % attr))
                    schema_ = serv.schema.get_by_name(schema)
                    if schema_:
                        should = {
                            "bool": {
                                "should": []
                            }
                        }
                        for attribute in schema_.attributes:
                            akey = "attributes.%s" % attribute["name"]
                            should["bool"]["should"].append({"term": {akey: attr}})
                        if should:
                            sub_query.append(should)
            for key, values in list(dict_attrs.items()):
                if with_wild:
                    for v in values:
                        if v.endswith("$") and v.startswith("^"):
                            v = v[1:-1]
                        v = v.replace("*", "")
                        sub_query.append({"match": {key: v}})
                else:
                    for v in values:
                        if v.endswith("$") and v.startswith("^"):
                            v = v[1:-1]
                        if v.startswith("*"):
                            v = v.replace("*", "")
                            sub_query.append({"match": {key: v}})
                        else:
                            sub_query.append({"term": {key: v}})

            if bool_type == "OR":
                body["filter"]["bool"]["should"] = body["filter"]["bool"]["should"] + sub_query
            else:
                body["filter"]["bool"]["must"] = body["filter"]["bool"]["must"] + sub_query

    return body


# 存放那些表有机房的字段
@cache.memoize(timeout=3600)
def get_schema_idc(schema):
    if not isinstance(schema, (list, tuple)):
        schema = [schema]
    result = False
    for ent in schema:
        schema_info_primeval = serv.schema.get_by_name(ent)
        if schema_info_primeval:
            schema_info = getattr(schema_info_primeval, "attributes")
            for sch in schema_info:
                if sch['name'] == 'idc':
                    result = True
                    break
    return result


# 存放机房账号，可以查看那些机房的信息
@cache.memoize(timeout=600)
def get_user_idc(um):
    has_filter = False
    idc_name = []
    auth_data = serv.entity.search_entity_terms("user", must={"um": [um]}, size=1)
    if len(auth_data) <= 0 or 'position' not in auth_data[0].attributes or len(
            auth_data[0].attributes['position']) <= 0:
        return idc_name
    # 查找组织
    auth_team = auth_data[0].attributes['team']
    if 'VIP服务中心' in auth_team:
        has_filter = True

    if has_filter:
        auth_position = auth_data[0].attributes['position'][0]
        match_list_str = auth_position.replace('(', '|').replace('（', '|').replace(')', '').replace('）', '')
        match_list = match_list_str.split('|')
        auth_belong_idc = serv.entity.search_entity_terms("idc", must={"group": match_list})
        for idc in auth_belong_idc:
            idc_name.append(idc.attributes['short_name'])

    return idc_name


@export("Idc")
def body_idc(schema, body, *args, **kwargs):
    if schema == "*":
        return body

    # 判断要查找的表格是否有IDC字段
    idc_exist = get_schema_idc(schema)
    if not idc_exist:
        return body
    um = body["g_user"]["um"]
    idc = get_user_idc(um)
    # 机房人员前端传机房字段值,也需要在限定的机房内；若在，返回所选的机房，若否，返回限定的机房
    if "attrs" in body:
        if "idc" in body["attrs"]:
            if len(idc) != 0 and body["attrs"]["idc"] in idc:
                return body

    # idc = ["Mega-I机房", "神舟机房"]
    if len(idc) != 0:
        body["filter"]["bool"]["must"].append({"terms": {"idc": idc}})
    return body
