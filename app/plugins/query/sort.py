# coding:utf-8

__author__ = 'Ti'


from app.utils.utils import export
from app import models
from sqlalchemy import func


@export("IpSort")
def sort_ip(key, value, *args, **kwargs):
    # TODO 多ip会正常？
    if value.get("order", "asc") == "desc":
        m = func.INET_ATON(models.EntityAttrVir.attr_vir_ip_ip).desc
        #m = func.INET_ATON(
        #    func.JSON_UNQUOTE(func.JSON_EXTRACT(models.Entity.attributes, "$.%s" % key))).desc
    else:
        m = func.INET_ATON(models.EntityAttrVir.attr_vir_ip_ip).asc
        #m = func.INET_ATON(
        #    func.JSON_UNQUOTE(func.JSON_EXTRACT(models.Entity.attributes, "$.%s" % key))).asc
    return m

