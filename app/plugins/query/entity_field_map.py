# coding:utf-8

__author__ = 'ti'

import app.models
from app.utils.utils import export


@export("Entity_id")
def entity_id(schema, *args, **kwargs):
    return app.models.Entity.id


@export("Entity_key")
def entity_key(schema, *args, **kwargs):
    return app.models.Entity.key


@export("Entity_primary")
def entity_primary(schema, *args, **kwargs):
    return app.models.Entity.primary


@export("Entity_schema")
def entity_schema(schema, *args, **kwargs):
    return app.models.Entity.schema


@export("Entity_attributes")
def entity_attributes(schema, *args, **kwargs):
    return app.models.Entity.attributes


