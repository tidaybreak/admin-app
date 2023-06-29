# coding:utf-8

import re
from app import ext
import time
import json
import random
import string
import hashlib
import inspect
import fnmatch
import io
import os
import collections
import linecache
from decimal import Decimal
from datetime import datetime, timedelta
import csv
import xlsxwriter
import codecs
import openpyxl
from io import BytesIO
from werkzeug.datastructures import ImmutableMultiDict
from flask import request
from uuid import uuid4
from decimal import Decimal
from functools import wraps
from flask import jsonify
from copy import deepcopy
from flask import g

__author__ = 'Ti'


def str2md5(str):
    str=str.encode(encoding='utf-8')
    md5=hashlib.md5(str).hexdigest()
    return md5


def view_cache_key(*args, **kwargs):
    """
    自定义缓存键:
        首页和归档页路由 url 是带参数的分页页数组成：/index?page=2
        flask-cache 缓存的 key_prefix 默认值获取 path ：/index
        需要自定义不同页面的 cache_key : /index/page/2
    """
    # 需要判断的key类表
    request_list = ['form', 'data', 'values', 'query_string']
    query_string = ""
    # 根据值的类型，判断是否为空，不为空则返回（若为空，不能区分不同的表格）
    for val in request_list:
        if hasattr(request, val):
            data_type = getattr(request, val)
            if isinstance(data_type, ImmutableMultiDict):
                query_data = data_type.to_dict(flat=False)
                if query_data:
                    query_string = str(query_data)
                    break
                continue
            if isinstance(data_type, bytes):
                query_data = str(data_type, encoding="utf-8")
                if query_data:
                    query_string = query_data
                    break
                continue
            # 保留作为字符串默认的判断方式，暂未发现该请求方式
            if isinstance(data_type, str):
                if data_type:
                    query_string = query_data
                    break
                continue

    path = hash_dict(request.path + query_string + g.user['um'])
    return path


def get_path_type():
    type_ = os.path.splitext(request.path)
    return type_[-1][1:]


def get_attrs_by_formatter(formatter_string):
    rr = formatter_string.replace("(", "\(")
    rr = rr.replace(")", "\)")
    re_formatter = re.findall(r'attributes\.(.*?)\]', rr)
    attributes = []
    for attr in re_formatter:
        attributes.append(attr.strip())
    return attributes


def get_attrs_by_formatter_values(formatter_string, value):
    """

    :param formatter_string:  u'{[ attributes.name ]}({[ attributes.um ]})'
    :param value: u'凌宇鹏(lingyp)'
    :return: [u'凌宇鹏', u'lingyp']
    """
    re_val = []
    new_formatter_string = formatter_string.replace("(", "\(")
    new_formatter_string = new_formatter_string.replace(")", "\)")
    re_formatter = re.findall(r'{(.*?)}', new_formatter_string)

    for ent in re_formatter:
        new_formatter_string = new_formatter_string.replace("{" + ent + "}", "(.*)?")
    re_match = re.match(r"%s" % new_formatter_string, value)
    if re_match:
        re_match_groups = re_match.groups()
        for ent in re_match_groups:
            re_val.append(ent)
    return re_val


def clean_ukey(um, cache):
    """
    清理用户相关的key
    :param um:
    :param cache:
    :return:
    """
    ukeys = "UserKeys:%s" % um
    ckeys = cache.get(ukeys)
    if ckeys:
        for key in ckeys:
            cache.delete(key)
    cache.set(ukeys, [])
    return True


def diff_attrs(data, prev):
    diffs = []
    for attr, value in list(data.items()):
        if prev.get(attr) != value:
            diffs.append(attr)
    return diffs


class JSONDict(dict):
    def __getattr__(self, item):
        try:
            res = self[item]
            if isinstance(res, dict):
                res = JSONDict(res)
            return res
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, key, value):
        self[key] = value

    def _default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        return json.JSONEncoder.default(o)

    def to_json(self, pretty=False):
        if not pretty:
            return json.dumps(self, default=self._default, sort_keys=True)
        else:
            return json.dumps(self, default=self._default, sort_keys=True, indent=4, separators=(',', ': '))

    @classmethod
    def from_json(cls, json_str):
        return json.loads(json_str, object_hook=lambda x: JSONDict(x))


def call_func(fn_, *args, **kwargs):
    """
    如果fn_不为空，就调用它，否则返回None
    :param fn_:
    :param args:
    :param kwargs:
    :return:
    """
    if fn_:
        return fn_(*args, **kwargs)


def resolve_path(module_, model, attr):
    """
    这里会从模块里面获取模型，再从模型里面获取属性
    :param module_:
    :param model:
    :param attr:
    :return:
    """
    model = getattr(module_, model.capitalize()) if (model and module_) else None
    if model:
        attr = getattr(model, attr)
        if attr:
            return model, attr


def rnd(length, lower=False):
    """
    获取随即字符串
    """
    if lower:
        return ''.join(random.sample(string.ascii_lowercase + string.digits, length))
    else:
        return ''.join(random.sample(string.ascii_letters + string.digits, length))


def uuid():
    return uuid4().hex


def gen_id():
    """
    生成一个唯一id
    :return:
    """
    return "N_%s" % uuid()


def add_x(q, with_wild=True):
    q = q.split(':')
    if with_wild:
        if q[-1].startswith("^"):
            q[-1] = q[-1][1:]
        else:
            if not q[-1].startswith("*"):
                q[-1] = "*%s" % q[-1]

        if q[-1].endswith("$"):
            q[-1] = q[-1][:-1]
        else:
            if not q[-1].endswith("*"):
                q[-1] = "%s" % q[-1]
    return ':'.join(q)


REG = re.compile(r" OR|AND ", re.I)


def parse_q(query):
    if query and query not in ["*", ""]:
        values1 = []
        values2 = {}
        for q in REG.split(query):
            item = q.split(":")
            if len(item) == 2:
                if "." in item[0]:
                    # attr = item[0].split(".")[-1]
                    attr = item[0]
                else:
                    attr = item[0]
                value = item[1]
                if attr in values2:
                    values2[item[0]].append(value.strip())
                else:
                    if not values2:
                        values2 = {attr: [value.strip()]}
                    else:
                        values2[attr] = [value.strip()]
            elif len(item) == 1:
                if not values1:
                    values1 = [item[0].strip()]
                else:
                    values1.append(item[0].strip())
            else:
                # IPv6需要中间有多个":"，因此，直接返回原来的字符
                if not values1:
                    values1 = [q.strip()]
                else:
                    values1.append(q.strip())

        if ' or ' in query or ' OR ' in query:
            return "OR", values1, values2
        else:
            return "AND", values1, values2


def parse_kwargs(args):
    """
    解析参数
    @param args string:例如：[key1=val1, key2=val2]
    @return (list,dict):
    e.g. {'val2': 'key2', 'val1': 'key1'}
    """
    if isinstance(args, str):
        args = args.split(',')
    r_kwargs = {}
    if args:
        for arg in args:
            regx = re.compile(r"([a-z0-9A-Z_-]+)=(.+)")
            kv = regx.findall(arg)
            if kv:
                r_kwargs.update({kv[0][0]: kv[0][1]})
    return r_kwargs


def export(export_name=None):
    """
    标识一个export
    :return:
    """

    def wrapper(func):
        func.__name__ = export_name or func.__name__
        func.export = True

        @wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        return inner

    return wrapper


def checkip(ip):
    if ip is not None:
        p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if p.match(ip):
            return True
        else:
            p2 = re.compile(
                '^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$')
            if p2.match(ip):
                return True
            else:
                return False

    return True


def build_query(q=None, attrs=None, pinyin=None, extra_query="", with_wild=True, sort=None, filter_=None,
                field_info=None):
    query = {}
    if not sort:
        query["sort"] = [{"key": {"order": "asc"}}]
    else:
        query["sort"] = sort
    query["query"] = {
        "filtered": {}
    }
    query_str = []
    attrs = attrs if attrs else []
    for attr in attrs:
        range_attr = {}
        if field_info and field_info.get("type") == "Date":
            value = attrs.get(attr, '').split(';')
            if value[0]:
                range_attr["from"] = value[0]
            if value[1]:
                range_attr["to"] = value[1]
        if range_attr:
            if "filter" not in query["query"]["filtered"]:
                query["query"]["filtered"]["filter"] = {"bool": {"must": []}}
            query["query"]["filtered"]["filter"]["bool"]["must"].append({
                "range": {
                    "attributes.%s" % attr: range_attr
                }
            })
        else:
            value = attrs.get(attr, None)
            if value is not None:
                if isinstance(value, list):
                    query1 = []
                    for v in value:
                        wild_val = add_x(v, with_wild)
                        if wild_val == "*":
                            wild_val = wild_val + " OR (NOT _exists_:attributes.%s)" % attr
                            query_ = "(attributes.%s:%s)" % (attr, wild_val)
                        else:
                            query_ = "attributes.%s:%s" % (attr, wild_val)
                        query1.append(query_)
                    query_str.append("(%s)" % " OR ".join(query1))
                else:
                    value = str(value).replace("--所有--", '*').replace("(", "\(").replace(")", "\)")
                    wild_val = add_x(value, with_wild)
                    if wild_val == "*":
                        wild_val = wild_val + " OR (NOT _exists_:attributes.%s)" % attr
                        query_ = "(attributes.%s:%s)" % (attr, wild_val)
                    else:
                        query_ = "attributes.%s:%s" % (attr, wild_val)
                    query_str.append(query_)
    if q:
        qstr = add_x(q, with_wild)
        qstr = str(qstr).replace("(", "\(").replace(")", "\)")
        if pinyin:
            qstr = "(%s OR %s)" % (qstr, add_x(pinyin, with_wild))
        query_str.append(qstr)
    if extra_query:
        query_str.append(extra_query)
    query["query"]["filtered"]["query"] = {
        "query_string": {"query": ' AND '.join(query_str), "lowercase_expanded_terms": False}}
    if filter_:
        query["query"]["filtered"].update(filter_)
    return query


def build_cache_key(type_, model, func=None, **kwargs):
    """
    把传进来的参数先进行自然排序，再进行一个key的构造，格式如：db:schema::get_schema::name=xxx,version=xxxx
    :param kwargs:
    :return:
    """
    keys = list(kwargs.keys())
    keys.sort()
    result = [type_, model]
    if func:
        result.append(func)
    others = []
    for key in keys:
        value = kwargs[key] if kwargs[key] is not None else ''
        others.append("%s=%s" % (key, value))
    if others:
        result.append(','.join(others))
    return "::".join(result)


def hash_obj(o):
    md5 = hashlib.md5()
    for k in sorted(dir(o)):
        if k.startswith('__'):
            continue
        a = getattr(o, k)
        if a is None:
            continue
        if inspect.isroutine(a):
            continue
        md5.update(bytes(k, encoding="utf8"))
        if isinstance(a, (tuple, set, list)):
            md5.update(hash_seq(a))
        elif isinstance(a, dict):
            md5.update(hash_dict(a))
        elif isinstance(a, (float, int, str, Decimal)):
            md5.update(str(a).encode(encoding='utf-8'))
        else:
            md5.update(hash_obj(a))
    return md5.hexdigest()


def hash_seq(l):
    md5 = hashlib.md5()
    for i in sorted(l):
        if isinstance(i, (tuple, set, list)):
            md5.update(hash_seq(i))
        elif isinstance(i, dict):
            md5.update(hash_dict(i))
        elif isinstance(i, (float, int, str, Decimal)):
            md5.update(str(i).encode(encoding='utf-8'))
        else:
            md5.update(hash_obj(i))
    return md5.hexdigest()


def hash_dict(d):
    return hashlib.md5(json.dumps(d, sort_keys=True).encode("utf-8")).hexdigest()


def mhash(data):
    if isinstance(data, dict):
        return hash_dict(data)
    elif isinstance(data, (tuple, set, list)):
        return hash_seq(data)
    elif isinstance(data, (float, int, str, Decimal)):
        md5 = hashlib.md5()
        md5.update(str(data).encode(encoding='utf-8'))
        return md5.hexdigest()
    else:
        return hash_obj(data)


def fattern_obj_attrs(attrs):
    """
    将type=Object字典的属性构造一个扁平字符串
    :param attrs:
    :return:
    """
    result = []
    for attr in attrs:
        result.append(attr["name"])
    return result


def fattern_attr_name(attr):
    return attr["name"]


def json_find(json_data, key):
    """
    从json中查找key对应的值，key如果有多层次，用点分割
    """

    def _find(json_, key_):
        result = []

        def _decode_dict(dict_):
            try:
                if isinstance(dict_[key_], (tuple, list, set)):
                    result.append(list(dict_[key_]))
                else:
                    result.append(dict_[key_])
            except KeyError:
                pass
            return dict_

        json.loads(json_, object_hook=_decode_dict)
        return result

    for k in key.split('.'):
        json_data = json.dumps(_find(json_data, k))
    return json.loads(json_data)


def dict_del_kv(dict_data, key):
    """
    从字典中查找key对应的值，并删除
    """
    parent = [dict_data]
    child = [dict_data]
    last_k = [key]

    def _find(dict_, key_, ):
        parent[0] = dict_
        if dict_:
            child[0] = dict_.get(key_)
        last_k[0] = key_

    for k in key.split('.'):
        _find(child[0], k)
    del parent[0][last_k[0]]
    return dict_data


def dict_with_kvs(dict_data, keys):
    """
    从字典中查找key对应的值，并返回
    """
    result = {}
    child = [dict_data] * len(keys)
    last_k = deepcopy(keys)
    tmp = [result]

    def _find(dict_, key_, i_):
        if isinstance(dict_, dict):
            child[i_] = dict_.get(key_)
        else:
            child[i_] = None
        last_k[i_] = key_

    for index, key in enumerate(keys):
        key = key.split('.')
        for i, k in enumerate(key):
            if (i + 1) < len(key):
                if tmp[0].get(k) is None:
                    tmp[0][k] = {}
                tmp[0] = tmp[0][k]
            _find(child[index], k, index)
        if child[index] is not None:
            tmp[0].update({last_k[index]: child[index]})
        tmp[0] = result

    return result


def flatten(d, parent_key='', sep='.', with_wild=False):
    items = []
    for k, v in list(d.items()):
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(list(flatten(v, new_key, sep=sep).items()))
        else:
            items.append((new_key, add_x(v) if with_wild else v))
    return dict(items)


def res_json(code, message="", data={}, success=True, **kwargs):
    """

    :param code:
    :param message:
    :param data:
    :param success: False:异步未完成 True:同步或异步完成
    :param kwargs:
    :return:
    """
    res = jsonify(
        code=code,
        data=data,
        message=message,
        success=success,
        **kwargs
    )
    if str(code) in ["200", "401", "403"]:
        res.status_code = code
    return res


def decision(allows, permissions):
    """
    针对传入的参数判断是否有权限
    :param allows:
    :param permissions:
    :return:
    """
    includes = [p for p in permissions if 'include' in p]
    excludes = [p for p in permissions if 'exclude' in p]
    in_priority = set([])
    ex_priority = set([])
    for item in allows:
        for i in includes:
            pattern, resource, priority = i.split(':')
            regx = re.compile(resource)
            if fnmatch.fnmatch(item, resource) or regx.match(item):
                in_priority.add(int(priority))
        for e in excludes:
            pattern, resource, priority = e.split(':')
            regx = re.compile(resource)
            if fnmatch.fnmatch(item, resource) or regx.match(item):
                ex_priority.add(int(priority))
    if in_priority:
        if ex_priority:
            return max(in_priority) > max(ex_priority)
        return True
    else:
        return False


def make_header(entity, is_show=None):
    """
    构造entity的搜索头
    :param entity:
    :return:
    """
    result = {
        "name": entity["name"],
        "display_name": entity["display_name"],
        "showable": is_show or entity["listable"],
        "searchable": entity["searchable"],
        "wildcard": True,
    }
    if entity["type"] == "Enum":
        result["type"] = "state"
        result["items"] = [{"name": "--所有--", "value": ""}]
        for item in entity["enum_item"]:
            result["items"].append({"name": item, "value": item})
    if getattr(entity, "wildcard", None) is not None:
        result["wildcard"] = entity["wildcard"]
    else:
        result["wildcard"] = True
    if getattr(entity, "is_user", None):
        result["type"] = "user"
    return result


def parse_attr(schema, content):
    """

    :return:
    """
    # 检查配置项结构是否正确
    s = io.StringIO()
    s.write(content)
    s.seek(0)

    lines = content.splitlines()
    line_index = 0
    line_len = 0
    mult_attrs = []
    if "," in lines[0]:
        split_ = ","
    else:
        split_ = "|"

    lines = []
    rdr = csv.reader(s, delimiter=split_, quotechar='"')
    for line in rdr:
        lines.append(line)

    attributes = []
    display_attrs = lines[0]
    attrs = {}
    for attr in schema.attributes:
        if attr["is_multi"]:
            mult_attrs.append(attr["name"])
        attrs[attr["display_name"]] = attr["name"]
    if not all([str(x) in attrs for x in display_attrs]):
        raise Exception("提供的字段错误，请在第一行指定录入信息字段")
    try:
        for index, line in enumerate(lines[1:]):
            tmp = {}
            line_index = index + 2
            line_len = len(line)
            for index, name in enumerate(display_attrs):
                attr = attrs[str(name)]
                if attr in mult_attrs:
                    tmp[attr] = []
                    if line[index]:
                        for item in line[index].split(";"):
                            tmp[attr].append(str(item))
                else:
                    tmp[attr] = str(line[index])
            attributes.append({"attributes": tmp})
    except IndexError:
        raise Exception("第%s行提供的数据字段数量为%s，应该要提供%s个" % (line_index, line_len, len(attrs)))
    return attributes


def parse_data(imeta, headers, rows):
    """

    :return:
    """
    headers_str = imeta.keys()
    attributes = []

    if not headers:
        raise Exception(u"请在第二行指定录入字段名称")

    extra = list(set(headers) - set(headers_str))

    if extra:
        raise Exception(u"第二行提供的字段'%s'在表中不存在，请删除后再提交" % ','.join(extra))
    try:
        for index, line in enumerate(rows):
            tmp = {}
            line_index = index + 3
            line_len = len(line)
            for index2, name in enumerate(headers):
                attr = imeta[name]["attr"]
                value = line[index2]
                if value is None:
                    if imeta[name]["require"]:
                        raise Exception(u"第%s行提供的字段'%s'数据不能为空" % (line_index, name))
                tmp[attr] = value
            attributes.append(tmp)
    except IndexError:
        raise
    return attributes

def can_datetime_format(datetime, format):
    try:
        time.strptime(datetime, format or "%Y-%m-%d %H:%M:%S")
        return True
    except:
        return False


def is_key_string(key):
    if key.startswith("N_") and len(key) == 34:
        return True
    else:
        return False


EXPR1 = re.compile("__([A-Z]+)__")


def get_expr_type(exprs):
    items = EXPR1.findall(exprs)
    if items:
        return items[0]


EXPR2 = re.compile("__EQ__|__IN__")


def parse_expr(exprs):
    items = EXPR2.split(exprs)
    if len(items) == 2:
        items.append(get_expr_type(exprs))
        return items
    else:
        return ["", "", None]


def reverse_dict(data):
    result = {}
    for key, value in list(data.items()):
        result[value] = key
    return result


def process_line_stats(line_stats):
    profile_results = []

    if not line_stats:
        return profile_results

    multiplier = line_stats.unit / 1e-3

    for key, timings in sorted(line_stats.timings.items()):
        if not timings:
            continue

        filename, start_lineno, func_name = key

        all_lines = linecache.getlines(filename)
        sublines = inspect.getblock(all_lines[start_lineno - 1:])
        end_lineno = start_lineno + len(sublines)

        line_to_timing = collections.defaultdict(lambda: (-1, 0))

        for (lineno, nhits, time) in timings:
            line_to_timing[lineno] = (nhits, time)

        padded_timings = []

        for lineno in range(start_lineno, end_lineno):
            nhits, time = line_to_timing[lineno]
            padded_timings.append((lineno, nhits, time))

        profile_results.append({
            'filename': filename,
            'start_lineno': start_lineno,
            'func_name': func_name,
            'timings': [
                (
                    lineno,
                    str(all_lines[lineno - 1].decode("utf8")),
                    time * multiplier,
                    nhits,
                ) for (lineno, nhits, time) in padded_timings
            ],
            'total_time': sum([time for _, _, time in timings]) * multiplier
        })

    return profile_results


def l2u(data):
    if isinstance(data, list):
        # 表格类型处理
        if len(data) == 2 and isinstance(data[0], str) and isinstance(data[1], list):
            data[1].sort()
            return data[0] + ",".join([str(l) for l in data[1]])
        else:
            data.sort()
            return ",".join([str(l) for l in data])
    else:
        return data


def diff_history(curr, prev):
    """

    :param curr:
    :param prev:
    :return:
    """
    prev_attrs = prev["attributes"]
    prev_attr_keys = list(prev_attrs.keys())

    curr_attrs = curr["attributes"]
    curr_attr_keys = list(curr_attrs.keys())

    result = {}
    delattrs = set(prev_attr_keys) - set(curr_attr_keys)
    if delattrs:
        result["delete"] = {}
    addattrs = set(curr_attr_keys) - set(prev_attr_keys)
    if addattrs:
        result["add"] = {}
    editattrs = set(curr_attr_keys) & set(prev_attr_keys)

    for attr in delattrs:
        result["delete"][attr] = l2u(prev_attrs[attr])

    for attr in addattrs:
        result["add"][attr] = l2u(curr_attrs[attr])

    for attr in editattrs:
        p = l2u(prev_attrs[attr])
        c = l2u(curr_attrs[attr])
        if p != c:
            if "edit" not in result:
                result["edit"] = {}
            result["edit"][attr] = [p, c]
    return result


def check_year_month(d):
    '''
    检查格式类似 2019-09
    :param d:
    :return: bool
    '''
    if len(d) != 7:
        return False
    dl = d.split("-")
    if len(dl) != 2:
        return False
    for i in dl:
        if not i.isdigit():
            return False
    return True

def isNone(s):
    return s is None

def get_first_and_last_date(year=None, month=None, obj=False):
    now = datetime.now()
    set_year = None
    set_month = None
    if year is not None and month is not None:
        set_year = year
        set_month = month
    elif year is not None:
        set_year = year
        set_month = now.month
    elif month is not None:
        set_year = now.year
        set_month = month
    else:
        set_year = now.year
        set_month = now.month

    first_date = datetime.strptime("{year}-{month}-01".format(year=set_year, month=set_month), "%Y-%m-%d")
    last_date = datetime.strptime(
        "{year}-{month}-01".format(year=set_year,
                                   month=set_month + 1
                                   ),
        "%Y-%m-%d") - timedelta(days=1)

    if obj:
        return first_date, last_date
    return first_date.strftime("%Y-%m-%d"), last_date.strftime("%Y-%m-%d")

def rounding(value):
    return Decimal(value).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")

def export(export_name=None):
    """
    标识一个export
    :return:
    """

    def wrapper(func):
        func.__name__ = export_name or func.__name__
        func.export = True

        @wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        return inner

    return wrapper