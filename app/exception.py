#coding:utf-8

__author__ = 'Ti'


class CMDBError(Exception):
    """
    这里可以定义一些系统常见的错误
    """
    pass

class TypeValueError(Exception):
    """
    这里可以定义字段类型值的常见错误
    """
    pass


class EntityError(Exception):
    """
    这里可以定义配置项的常见错误
    """
    pass


class IndexError(Exception):
    """
    ES索引遇到错误了
    """
    pass

class DBError(Exception):
    """
    DB遇到错误了
    """
    pass
