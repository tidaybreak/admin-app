# coding:utf-8

__author__ = ''

import re
from app import ext
from app import models
import traceback
from app.utils.utils import resolve_path
from app.db.elastic_query import elastic_query

# 这里会匹配get_<model>_by_<attr>这种格式的调用
REGX = re.compile(r'get_([a-z_]+)_by_([a-z_]+)')
# 创建一个值为弱引用的字典，它的值可能随时会被gc回收，可以用来做cache
CACHE = {}


class DBAccess(object):
    """
    数据库基础类，尽可能在这个地方把通用性很强的数据访问接口写在这里
    """

    def __getattr__(self, item):
        """
        这个并不是做数据缓存
        通过这个接口获取:self.db
        拦截返回一些通用未在类里定义的函数，比如get_schema_by_name后缀的函数调用 调用方法：self.schema.get_by_name("server")
        :return model
        """
        # 如果已经cache了就不用

        if CACHE.get(item):
            return CACHE[item]
        search = REGX.search(item)
        if search:
            model, attr = search.groups() if search else ['', '']
            model_attr = resolve_path(models, model, attr)
            if model_attr:
                # 返回通过ID获取的记录,scalar函数一旦有返回第一个，如果没有则返回None
                def get_query(id_):
                    data = ext.db.session.query(model_attr[0]).filter(model_attr[1] == id_).all()
                    if len(data) == 1:
                        return data[0]
                    elif len(data) == 0:
                        return
                    else:
                        return data

                CACHE[item] = get_query
                return CACHE[item]
        else:
            return getattr(models, item)

    def get_query(self, obj):
        """
        传入一个模型，例如：user，这里就会查询User模型
        """
        # obj = getattr(models, obj.capitalize())
        obj = getattr(models, obj)
        result = []
        if obj:
            result = self.db.session.query(obj)
        return result

    def get_model(self, obj):
        """
        传入一个模型，例如：user，这里就会查询User模型
        """
        # obj = getattr(models, obj.capitalize())
        return getattr(models, obj)

    def bulk_save(self, cls_str, conds):
        '''
        批量插入
        :param cls: 模型类
        :param conds: 插入的模型字段字典列表
        :return:
        '''
        try:
            cls = getattr(models, cls_str)
            self.db.session.bulk_insert_mappings(
                cls,
                conds
            )
            self.db.session.commit()
            return True, "ok"
        except Exception:
            # 回滚
            self.db.session.rollback()
            traceback.print_exc()
            return False, traceback.format_exc()

    def bulk_update(self, cls_str, conds):
        '''
        批量更新
        :param cls: 模型类
        :param conds: 插入的模型字段字典列表
        :return:
        '''
        try:
            cls = getattr(models, cls_str)
            self.db.session.bulk_update_mappings(
                cls,
                conds
            )
            self.db.session.commit()
            return True, "ok"
        except Exception:
            # 回滚
            self.db.session.rollback()
            traceback.print_exc()
            return False, traceback.format_exc()

    def delete(self, cls_str, id):
        try:
            cls = getattr(models, cls_str)
            self.db.session.query(cls).filter_by(id=id).delete()
            self.db.session.commit()
            return True, "ok"
        except Exception:
            # 回滚
            self.db.session.rollback()
            traceback.print_exc()
            return False, traceback.format_exc()

    def update(self, cls_str, query_dict={}, update_dict={}, insert=False):
        try:
            cls = getattr(models, cls_str)
            # self.db.session.query(cls).filter_by(**query_dict).update(update_dict)
            call = self.db.session.query(cls).filter_by(**query_dict)
            call_stats = call.first()
            if call_stats:
                # 更新行
                call.update(update_dict)
                self.db.session.commit()
            elif insert:
                # 插入新行
                query_dict.update(update_dict)
                self.bulk_save(cls_str, [query_dict])

            return True, "ok"
        except Exception:
            # 回滚
            self.db.session.rollback()
            traceback.print_exc()
            return False, traceback.format_exc()

    def elastic_query(self, model, query_dict={}):
        '''
        """ test simple query """
        query_string = '{"filter" : {"uid" : {"like" : "%1957%"} } }'
        query_string = '{"filter" : {"name" : {"like" : "%Jho%"}, "lastname" : "Galt" } }'

        """ test and operator """
        query_string = '{"filter" : {"and" : {"name" : {"like" : "%Jho%"}, "lastname" : "Galt", "uid" : {"like" : "%1957%"} } } }'

        """ test or operator """
        query_string = '{"filter" : {"or" : { "name" : "Jobs", "lastname" : "Man", "uid" : "19571957" } } }'

        """ test or and operator """
        query_string = '{"filter" : {"or" : { "name" : "Jhon", "lastname" : "Galt" }, "and" : { "uid" : "19571957" } } }'

        """ test operator levels """
        query_string = '{"filter" : {"or" : { "name" : "Jhon", "lastname" : "Man" } }, "sort": { "name" : {"order": "asc", "idx": 1} } }'

        """ test operator in """
        query_string = '{"filter" : {"name" : {"in" : ["Jhon", "Peter", "Iron"] } } }'

        """ test allow_fields option """
        query_string = '{"filter" : {"or" : { "name" : "Jhon", "lastname" : "Man" } }, "sort": { "name" : {"order": "asc", "idx": 1} } }'

        """ test search for levels """
        query_string = '{"filter" : {"or" : { "city.name" : "New York", "lastname" : "Man" } }, "sort": { "name" : {"order": "asc", "idx": 1} } }'
        '''

        return elastic_query(model, query_dict, self.db.session)

    def execute(self, raw_sql, params):
        try:
            resultproxy = self.db.session.execute(raw_sql, params)
            if resultproxy.returns_rows:
                return resultproxy.fetchall()
            self.db.session.commit()
            return resultproxy.rowcount
        except Exception:
            # 回滚
            self.db.session.rollback()
            traceback.print_exc()
            return False, traceback.format_exc()
