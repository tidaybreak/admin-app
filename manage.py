#!env python
# coding=utf-8


try:
    import warnings
    from flask.exthook import ExtDeprecationWarning

    warnings.simplefilter('ignore', ExtDeprecationWarning)
except ImportError as err:
    pass

import builtins
import imp
from dotenv import load_dotenv

load_dotenv('.env')

try:
    import line_profiler
    profiler = line_profiler.LineProfiler()

    def profile(func):
        global profiler
        global cache
        profiler.add_function(func)

        def inner(*args, **kwargs):
            try:
                res = functools.partial(profiler.runcall, func)(*args, **kwargs)
                return res
            except Exception as err:
                raise Exception(traceback.format_exc())
            finally:
                processed_line_stats = process_line_stats(profiler.get_stats())
                if cache and processed_line_stats:
                    cache.set("PROFILE:TOOL:CACHE", processed_line_stats)

        return inner
except ImportError as err:
    print(str(err))
    profile = lambda x: x

builtins.__dict__["profile"] = profile

import sys
import functools
import traceback
import requests, json
from copy import deepcopy
from app.config import cfg
from termcolor import colored as c
from prettytable import PrettyTable
from flask_script import Manager, Shell
from flask import current_app
from flask_migrate import Migrate, MigrateCommand
from app.settings import create_app, configure_blueprints
from app.ext import db, redis, celery, serv
from app.utils.utils import process_line_stats

imp.reload(sys)
#sys.setdefaultencoding('utf-8')

app = create_app(conf=cfg)
import app.routers as routers
app = configure_blueprints(app, routers.MOUNT_POINTS)
#app = configure_blueprints(app, [])

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, cache=cache, redis=redis, serv=serv, celery=celery)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

@manager.command
def create_all():
    """
    create all database tables
    """
    db.create_all()


@manager.command
def clean_redis():
    prefix = current_app.config["CACHE_KEY_PREFIX"]
    for key in redis.keys("%s*" % prefix):
        redis.delete(key)


@manager.command
def cache_formatter():
    formatters = serv.entity.dbaccess.get_all_reference_formatters()
    for key in formatters:
        ckey = "reference_formatter:%s" % key
        cache.set(ckey, formatters[key], timeout=24 * 3600 * 30)


@manager.command
def drop_all():
    """

    {"bandwidth":100,"bandwidth_property":"保底","billing_type":"95计费","line_type":"单线","note":"","price":120000,"upper_limit":1000}
    create all database tables
    """
    db.drop_all()


@manager.command
def rsync_catalog():
    headers = {
        "x-secretid": "nhchkywdix357rwd",
        "x-signature": "2948b1565a333b1b42c913c918633f40",
        "Content-Type": "application/json"
    }

    result = requests.get(
        "https://cmdb.ofidc.com/resource/v1/catalog/all.json",
        headers=headers
    ).json()

    if result["code"] == 200:
        catalog_ = result["data"]
        for catalog in catalog_:
            print((serv.catalog.save(catalog)))


@manager.option('-s', '--schema', dest="schema", help='specify schema to sync')
def rsync_schema(schema=None):

    headers = {
        "x-secretid": "nhchkywdix357rwd",
        "x-signature": "2948b1565a333b1b42c913c918633f40",
        "Content-Type": "application/json"
    }
    if schema is None:
        result = requests.get(
            "https://cmdb.ofidc.com/resource/v1/schema/all.json",
            headers=headers
        ).json()

        if result["code"] == 200:
            schemas = result["data"]
            for schema in schemas:
                print((serv.schema.save(schema)))
    else:
        result = requests.get(
            "https://cmdb.ofidc.com/resource/v1/schema/get.json?name=%s" % schema,
            headers=headers
        ).json()

        if result["code"] == 200:
            schema_ = result["data"]
            print((serv.schema.save(schema_)))


@manager.option('-s', '--schema', dest="schema", help='specify schema to sync')
@manager.option('-c', '--clean', dest="is_clean", help='specify clean schema data first if there have entity',
                action="store_true", default=False)
def rsync_entity(schema, is_clean):
    headers = {
        "x-secretid": "nhchkywdix357rwd",
        "x-signature": "2948b1565a333b1b42c913c918633f40",
        "Content-Type": "application/json"
    }
    print("start req....")
    result = requests.post(
        "https://cmdb.ofidc.com/resource/v1/entity/search.json?schema=%s" % schema,
        headers=headers,
        data=json.dumps({"schema": schema, "page_size": 100000})
    ).json()
    print("end req...")
    if result["code"] == 200:
        print(("start sync entity '%s' ..." % schema))
        if is_clean:
            serv.entity.clean(schema)
        entities = result["data"]["content"]
        if entities:
            print((serv.entity.msave(entities)))
            serv.entity.create_schema_rds(schema, is_clean=True)
        print(("end sync entity '%s'" % schema))


@manager.option('-a', '--all', dest="is_show_all", help='show all the line of profile functions.', action="store_true",
                default=False)
def debugtool(is_show_all):
    processed_line_stats = cache.get("PROFILE:TOOL:CACHE")
    if not processed_line_stats:
        return
    for function_result in processed_line_stats:
        print((c("#" * 100, "green")))
        print((c("{0} in {1}:{2}".format(
            function_result["func_name"],
            function_result["filename"],
            function_result["start_lineno"]
        ), "yellow")))
        print((c("Total Time:%.2f  ms" % function_result["total_time"])))
        print((c("#" * 100, "green")))
        table = PrettyTable(["Line", "    ", "% Time", "Time (ms)", "Hits"], caching=False)
        table.align["    "] = "l"
        table.padding_width = 1
        for lineno, line, timing, nhits in function_result["timings"]:
            perc = 100 * timing / function_result["total_time"]
            if perc > 10:
                tr_class = 'red'
            elif perc > 1:
                tr_class = 'yellow'
            else:
                tr_class = "white"

            if nhits != -1:
                perc = "%.1f" % perc
                timing = "%.1f" % timing
                nhits = nhits
            else:
                perc = " "
                timing = " "
                nhits = " "
            if tr_class == "white":
                if not is_show_all:
                    continue
            row = [lineno, c(line.rstrip(), tr_class), c(perc, tr_class), c(str(timing), tr_class),
                   c(str(nhits), tr_class)]
            table.add_row(row)

        print((table.get_string()))


@manager.command
def misc():
    data = """
D201707016318 70
D201707016320 10
    """
    headers = {
        "x-secretid": "nhchkywdix357rwd",
        "x-signature": "2948b1565a333b1b42c913c918633f40",
        "Content-Type": "application/json"
    }

    for line in data.strip().splitlines():
        item = line.split()
        if len(item) != 2:
            continue
        result = requests.post(
            "https://crm.ofidc.com/resource/v2/demand/variable/update.json",
            headers=headers,
            data=json.dumps({"demand_id": item[0], "name": "bandwidth", "value": int(item[1])})
        ).json()
        if not result["code"] == 200:
            print(("%s billing_type=%s fail:%s" % (item[0], item[1], result["message"])))


@manager.option('-s', '--schema', dest="schema", help='specify schema to sync')
def fix_resource(schema):
    """
    """
    if not schema:
        return
    headers = {
        "x-secretid": "nhchkywdix357rwd",
        "x-signature": "2948b1565a333b1b42c913c918633f40",
        "Content-Type": "application/json"
    }

    attrs = [{
        "enum": None,
        "form": {
            "init": None,
            "name": "demand_id",
            "size": None,
            "type": "Input",
            "lname": "需求编号",
            "multi": False,
            "width": None,
            "lwidth": None,
            "popover": "",
            "visible": True,
            "required": False,
            "placeholder": "请输入需求编号"
        },
        "name": "demand_id",
        "tags": [],
        "type": "String",
        "order": 3,
        "format": None,
        "length": None,
        "default": None,
        "is_user": False,
        "is_multi": False,
        "listable": False,
        "wildcard": True,
        "enum_item": [],
        "formatter": None,
        "is_unique": False,
        "reference": None,
        "schema_id": 192,
        "is_primary": False,
        "searchable": True,
        "description": None,
        "dynamic_job": None,
        "is_required": False,
        "parent_attr": None,
        "display_name": "需求编号",
        "dynamic_cron": None,
        "enum_generator": None,
        "is_form_hidden": True,
        "disable_edit": False,
        "reference_filter": None,
        "dynamic_cron_kwargs": None,
        "reference_formatter": None,
        "dynamic_fail_timeout": None
    }, {
        "enum": None,
        "form": {
            "init": None,
            "name": "order_id",
            "size": None,
            "type": "Input",
            "lname": "订单编号",
            "multi": False,
            "width": None,
            "lwidth": None,
            "popover": "",
            "visible": True,
            "required": False,
            "placeholder": "请输入订单编号"
        },
        "name": "order_id",
        "tags": [],
        "type": "String",
        "order": 2,
        "format": None,
        "length": None,
        "default": None,
        "is_user": False,
        "is_multi": False,
        "listable": False,
        "wildcard": True,
        "enum_item": [],
        "formatter": None,
        "is_unique": False,
        "reference": None,
        "schema_id": 192,
        "is_primary": False,
        "searchable": True,
        "description": None,
        "dynamic_job": None,
        "is_required": False,
        "parent_attr": None,
        "display_name": "订单编号",
        "dynamic_cron": None,
        "enum_generator": None,
        "is_form_hidden": True,
        "disable_edit": False,
        "reference_filter": None,
        "dynamic_cron_kwargs": None,
        "reference_formatter": None,
        "dynamic_fail_timeout": None
    }]

    schema_ = serv.schema.get_by_name(schema)
    attributes = deepcopy(schema_.attributes)
    has_order_id = False
    for ent in attributes:
        if ent["name"] == "order_id":
            has_order_id = True
            break

    if not has_order_id:
        for index, ent in enumerate(schema_.attributes):
            if ent["name"] == "instance_id":
                for i in attrs:
                    attributes.insert(index, i)
        schema_.attributes = attributes
        db.session.add(schema_)
        try:
            db.session.commit()
        except:
            print((traceback.format_exc()))
            db.session.rollback()
            return

    res = requests.post(
        "http://order-app:8000/resource/v1/product/all.json",
        headers=headers).json()

    products = {}
    for item in res.get("data", []):
        products[item["schema"]] = item["product_name"]
    print(("get products", len(products)))
    instances = {}
    res = requests.post("http://order-app:8000/resource/v1/instance/all.json", headers=headers,
                        data=json.dumps({"product_name": [products[schema]]})).json()

    for ent in res.get("data", []):
        resource_key = ent["resource_key"]
        if resource_key:
            instances[resource_key] = {"demand_id": ent["demand_id"], "order_id": ent["order_id"]}
    print(("get instances", len(instances)))
    entities = serv.entity.get_all_entity(schema)
    print(("get resource", len(entities)))
    for ent in entities:
        attributes = deepcopy(ent.attributes)
        resource_key = ent.key
        v = instances.get(resource_key)
        if v:
            attributes.update(v)
        ent.attributes = attributes
        db.session.add(ent)
    try:
        print("start commit")
        db.session.commit()
    except:
        db.session.rollback()
        print((traceback.format_exc()))
    print("end.")


@manager.command
def xls():
    def main():
        import openpyxl
        wb = openpyxl.load_workbook("/Users/lufeng/Desktop/user.xlsx")
        st = wb.get_sheet_by_name(wb.active.title)
        headers = [r.value for r in st[2]]
        rows = []
        for n in range(3, st.max_row + 1):
            cls = []
            for cl in st[n]:
                cls.append(cl.value)
            if any(cls):
                rows.append(cls)
        schema = "user"
        schema_ = serv.schema.get_by_name(schema)
        attributes = serv.entity.parse_file_value(schema_, headers, rows)
        data = []
        for attribute in attributes:
            data.append({
                "schema": schema,
                "attributes": attribute["attributes"]
            })
        result, message = serv.entity.save_entity(schema_, data, skip_check=False)
        print((result, message))

    main()


@manager.option('-s', '--schema', dest="schema", help='specify schema to fix')
def fix_uniques(schema=None):
    schemas = []
    schemas_ = serv.schema.get_all_schema()
    for s in schemas_:
        if not schema:
            schemas.append(s)
        else:
            if schema == s.name:
                schemas.append(s)

    for schema in schemas:
        print((schema.name, serv.entity.fix_uniques(schema)))


@manager.option('-l', '--loginc', dest="loginc", help='')
@manager.option('-s', '--schema', dest="schema", help='specify schema to fix')
def fix_data(schema=None, loginc=10):
    schemas = []
    if not schema:
        #redis.delete("references")
        schemas_ = serv.schema.get_all_schema()
        for s in schemas_:
            if s.name != 'ip':
                schemas.append(s.name)
                print(("schemas:%s" % (s.name)))

        schemas.append('ip')
    else:
        schemas = [schema]
    for schema in schemas:
        print(schema)
        print((serv.repair.fix_data(schema, loginc=loginc)))


@manager.option('-s', '--schema', dest="schema", help='specify schema to fix')
def fix_schema(schema=None):
    print((serv.repair.repair_all_schema(schema)))


@manager.command
def create_receipt_account():
    accounts = """
10582	广东奥飞数据科技股份有限公司	人民币	B002
10173	广东奥飞数据科技股份有限公司	人民币	B004
11032	奥飞数据国际有限公司	人民币	B010
11444	广东奥飞数据科技股份有限公司	人民币	B004
11444	广东奥飞数据科技股份有限公司	人民币	B004
10850	广州奥佳软件技术有限公司	美元	B008
11444	广东奥飞数据科技股份有限公司	人民币	B004
11032	奥飞数据国际有限公司	人民币	B010
10114	广东奥飞数据科技股份有限公司	人民币	B004
10559	广东奥飞数据科技股份有限公司	人民币	B004
10173	广东奥飞数据科技股份有限公司	人民币	B004
10953	奥飞数据国际有限公司	人民币	B012
10006	广东奥飞数据科技股份有限公司	人民币	B001
11366	广东奥飞数据科技股份有限公司	人民币	B004
11032	奥飞数据国际有限公司	人民币	B010
10428	奥飞数据国际有限公司	美元	B004
10569	奥飞数据国际有限公司	人民币	B005
11260	广东奥飞数据科技股份有限公司	人民币	B004
10233	奥飞数据国际有限公司	人民币	B012
10233	奥飞数据国际有限公司	人民币	B012
11032	奥飞数据国际有限公司	人民币	B010
11032	奥飞数据国际有限公司	人民币	B010
11399	广东奥飞数据科技股份有限公司	人民币	B002
11411	广东奥飞数据科技股份有限公司	人民币	B004
11422	广东奥飞数据科技股份有限公司	人民币	B001
11282	广东奥飞数据科技股份有限公司	人民币	B001
11430	广州市昊盈计算机科技有限公司	人民币	B006
11409	广东奥飞数据科技股份有限公司	人民币	B005
    """
    headers = {
        "x-secretid": "nhchkywdix357rwd",
        "x-signature": "2948b1565a333b1b42c913c918633f40",
        "Content-Type": "application/json"
    }
    print("start req....")
    entities = []
    schema = "customer_receipt_account"
    result = requests.post(
        "https://cmdb.ofidc.com/resource/v1/entity/search.json?schema=%s" % schema,
        headers=headers,
        data=json.dumps({"schema": schema, "page_size": 100000})
    ).json()
    print("end req...")
    prevs = []
    currs = []
    if result["code"] == 200:
        for ent in  result["data"]["content"]:
            prevs.append("%(customer_id)s-%(company_main_body)s-%(money_unit)s-%(receipt_acc_id)s" % ent["attributes"])

    for line in accounts.strip().splitlines():
        customer_id, company_main_body, money_unit, receipt_acc_id = line.split()
        temp = {
            "schema": schema,
            "attributes": {
                "customer_id": customer_id,
                "company_main_body": company_main_body,
                "money_unit": money_unit,
                "receipt_acc_id": receipt_acc_id
            },
        }
        ukey = "%(customer_id)s-%(company_main_body)s-%(money_unit)s-%(receipt_acc_id)s" % temp["attributes"]
        if ukey not in prevs and ukey not in currs:
            currs.append(ukey)
            entities.append(temp)
    result = requests.post(
        "https://cmdb.ofidc.com/resource/v1/entity/msave.json",
        headers=headers,
        data=json.dumps({"body": entities, "schema": schema})
    ).json()
    print(("end req, entities=", len(entities), ", prevs=", len(prevs), json.dumps(result, ensure_ascii=False)))


if __name__ == '__main__':
    #route_init()
    manager.run(default_command="runserver")
