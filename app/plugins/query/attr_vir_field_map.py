# coding:utf-8

__author__ = 'ti'

import app.models
from app.utils.utils import export


@export("Attr_ip")
def attr_ip(schema, *args, **kwargs):
    return app.models.EntityAttrVir.attr_vir_ip_ip


@export("Attr_idc")
def attr_idc(schema, *args, **kwargs):
    return app.models.EntityAttrVir.attr_vir_idc_short_name


@export("Attr_uid")
def attr_uid(schema, *args, **kwargs):
    if schema == "customer":
        return app.models.EntityAttrVir.attr_vir_customer_uid
    else:
        return app.models.Entity.attributes["uid"]


@export("Attr_short_name")
def attr_short_name(schema, *args, **kwargs):
    if schema == "idc":
        return app.models.EntityAttrVir.attr_vir_idc_short_name
    elif schema == "customer":
        return app.models.EntityAttrVir.attr_vir_customer_short_name
    else:
        return app.models.Entity.attributes["short_name"]


@export("Attr_resource_id")
def attr_resource_id(schema, *args, **kwargs):
    if schema == "cabinet":
        return app.models.EntityAttrVir.attr_vir_cabinet_resource_id
    else:
        return app.models.Entity.attributes["resource_id"]


@export("Attr_name")
def attr_name(schema, *args, **kwargs):
    if schema == "user":
        return app.models.EntityAttrVir.attr_vir_user_name
    else:
        return app.models.Entity.attributes["name"]


@export("Attr_um")
def attr_um(schema, *args, **kwargs):
    if schema == "user":
        return app.models.EntityAttrVir.attr_vir_user_um
    else:
        return app.models.Entity.attributes["um"]
