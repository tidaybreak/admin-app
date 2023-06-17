# coding:utf-8

__author__ = 'ti'

from app.utils.utils import export


@export("Schema_depot_log")
def schema_depot_log(body, *args, **kwargs):
    auto_inc_sort = [{
        "goods_type": {
            "order": "asc"
        }
    },
    {
        "__auto_inc__": {
            "order": "asc"
        }
    }]
    if not body["sort"]:
        body["sort"] = []
    body["sort"] = body["sort"] + auto_inc_sort

    return body
