__author__ = 'Ti'

import os
import threading

import sqlalchemy
import time

from app import ext
from app.db.dbaccess import DBAccess
from app.loader import load_plugins
from sqlalchemy.engine import reflection


class BaseService(object):
    def __init__(self):
        self.model_name = "M" + self.__class__.__name__.split("Service")[0]
        self.redis = ext.redis
        self.serv = ext.serv
        self.plugins = self.load_plugins(ext.db.app)
        self.dbaccess = DBAccess()
        self.mutex = threading.Lock()
        self.columns_list = []
        # 获取表结构
        '''
        self.columns = 
        [{
            "autoincrement": false, 
            "comment": null, 
            "default": "'0'", 
            "name": "id", 
            "nullable": false, 
            "type": "INTEGER"
          }, 
          {
            "comment": null, 
            "default": null, 
            "name": "key", 
            "nullable": false, 
            "type": "VARCHAR"
          }]
        '''
        engine = ext.db.engine
        mod = self.dbaccess.get_model(self.model_name)
        table_name = mod.__tablename__
        columns_info = mod.columns_info()
        # 主键、表结构
        self.primary_key_columns = reflection.Inspector.from_engine(engine).get_pk_constraint(table_name)[
            'constrained_columns']
        self.columns = reflection.Inspector.from_engine(engine).get_columns(table_name)
        for idx, val in enumerate(self.columns):
            self.columns[idx]['id'] = idx
            self.columns[idx]['show'] = 1
            self.columns[idx]['edit'] = 0
            self.columns[idx]['sort'] = 0
            self.columns[idx]['search'] = 0
            self.columns[idx]['title'] = val['comment']
            self.columns_list.append(val['name'])
            if val['name'] in columns_info:
                self.columns[idx] = {**self.columns[idx], **columns_info[val['name']]}
        for key in columns_info:
            if key not in self.columns_list:
                columns_info[key]['name'] = key
                self.columns.append(columns_info[key])

    @staticmethod
    def load_plugins(app):
        plugins = {}
        for name in os.listdir(os.path.join(os.path.dirname(os.path.dirname(__file__)), "plugins")):
            plugins[name] = load_plugins(name, app)
        return plugins

    def query(self):
        return self.dbaccess.get_query(self.model_name)

    def model(self):
        return self.dbaccess.get_model(self.model_name)

    def find_one(self, query, to_type=""):
        query_dict = {
            "filter": query
        }
        items = self.fetch_list(query_dict=query_dict, to_type=to_type)["items"]
        if len(items) > 0:
            return items[0]
        else:
            return None

    def delete(self, id):
        primary_key = 'id'
        if len(self.primary_key_columns) > 0:
            primary_key = self.primary_key_columns[0]
        return self.dbaccess.delete(self.model_name, id, key=primary_key)

    def fetch_list(self,
                   page=1,
                   limit=None,
                   query_dict={},
                   to_type="dict",
                   field_info=False,
                   select=[]):

        # [全局]过滤&加工data 如[上传文件导入]操作
        op_args = {
            "schema": self.model_name,
            'columns_list': self.columns_list
        }
        query_dict = self.plugins["operate"].get("HookGlobal",
                                                 lambda x, _: x)(query_dict, op_args)

        return self.fetch(page=page,
                          limit=limit,
                          query_dict=query_dict,
                          to_type=to_type,
                          field_info=field_info,
                          select=select)

    def fetch(self, page=1,
              limit=None,
              query_dict={"filter": {}},
              to_type="dict",
              field_info=False,
              select=[]):

        """
        获取分页数据
        :param select:
        :param field_info:
        :param page:
        :param limit:
        :param query_dict:
        {
            "filter" : {
                "or" : {
                    "firstname" : {
                        "equals" : "Jhon"
                    },
                    "lastname" : "Galt",
                    "uid" : {
                        "like" : "111111"
                    }
                },
                "and" : {
                    "status" : "active",
                    "age" : {
                        "gt" : 18,
                        "lte" : 20
                    }
                }
            },
            "sort" : {
                "firstname" : {
                    "order": "asc",
                    "idx": 0
                },
                "age" : {
                    "order": "desc",
                    "idx": 1
                }
            }
        }
        # test simple query #
        query_string = '{"filter" : {"uid" : {"like" : "%1957%"} } }'
        query_string = '{"filter" : {"name" : {"like" : "%Jho%"}, "lastname" : "Galt" } }'

        # test and operator #
        query_string = '{"filter" : {"and" : {"name" : {"like" : "%Jho%"}, "lastname" : "Galt", "uid" : {"like" : "%1957%"} } } }'

        # test or operator #
        query_string = '{"filter" : {"or" : { "name" : "Jobs", "lastname" : "Man", "uid" : "19571957" } } }'

        # test or and operator #
        query_string = '{"filter" : {"or" : { "name" : "Jhon", "lastname" : "Galt" }, "and" : { "uid" : "19571957" } } }'

        # test operator levels #
        query_string = '{"filter" : {"or" : { "name" : "Jhon", "lastname" : "Man" } }, "sort": { "name" : {"order": "asc", "idx": 1} } }'

        # test operator in #
        query_string = '{"filter" : {"name" : {"in" : ["Jhon", "Peter", "Iron"] } } }'

        # test allow_fields option #
        query_string = '{"filter" : {"or" : { "name" : "Jhon", "lastname" : "Man" } }, "sort": { "name" : {"order": "asc", "idx": 1} } }'

        # test search for levels #
        query_string = '{"filter" : {"or" : { "city.name" : "New York", "lastname" : "Man" } }, "sort": { "name" : {"order": "asc", "idx": 1} } }'
        :param to_type:
        :return:
        """
        # print("mutex-acquire  %s %s  %s  %s  %s" % (os.getpid(), pid, t.ident, t.getName(), self.mutex))
        entities = []
        total = -1
        try:
            query = self.dbaccess.elastic_query(self.model(), query_dict)
            total = query.count()

            # print("start datetime:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            if limit is not None:
                query = query.offset((page - 1) * limit).limit(limit)
            if len(select) == 0:
                entities = query.all()
            else:
                entities = query.options(
                    sqlalchemy.orm.load_only(*select)
                ).all()
            # print("end datetime:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        except Exception as e:
            # print("db error:", e)
            raise e

        to_type = to_type.split('.')
        if to_type[0] == 'map':
            mkey = 'id'
            if len(to_type) == 2:
                mkey = to_type[1]
            data = {}
            for entity in entities:
                item = entity.dict()
                if mkey in item:
                    data[item[mkey]] = item
        elif to_type[0] == 'dict':
            items = []
            for entity in entities:
                items.append(entity.dict())
            data = {
                "total": total,
                "items": items
            }
        else:
            data = {
                "total": total,
                "items": entities
            }
        if field_info:
            data["columns"] = self.columns
        return data

    def insert(self, cond, action='add'):
        data = {}
        for ent in self.columns_list:
            if ent in cond:
                data[ent] = cond[ent]
        for ent in ['update_time', 'create_time']:
            if ent in data:
                del data[ent]
        return self.dbaccess.insert(self.model_name, data, action=action)

    def update(self, query_dict={}, update_dict={}, insert=False):
        data = {}
        for ent in self.columns_list:
            if ent in update_dict:
                data[ent] = update_dict[ent]
        for ent in ['update_time', 'create_time']:
            if ent in data:
                del data[ent]
        return self.dbaccess.update(self.model_name, query_dict, data, insert=insert)

    def bulk_save(self, conds, ingore_exist=None):
        self.mutex.acquire()
        result = None
        try:
            # if ingore_exist:
            #     self.dbaccess.query_in(ingore_exist)

            new_data = []
            for item in conds:
                data = {}
                for k in self.columns_list:
                    if k in item:
                        data[k] = item[k]
                for k2 in ['update_time', 'create_time']:
                    if k2 in data:
                        del data[k2]
                if len(data) > 0:
                    new_data.append(data)
            result = self.dbaccess.bulk_save(self.model_name, conds)
        except Exception as e:
            print("db error:", e)
        self.mutex.release()
        return result

    def bulk_update(self, conds):
        self.mutex.acquire()
        result = None
        try:
            result = self.dbaccess.bulk_update(self.model_name, conds)
        except Exception as e:
            print("db error:", e)
        self.mutex.release()
        return result

    def execute(self, raw_sql, params):
        """
        效率高 2-3倍
        :param raw_sql:
        :param params:
        :return:
        """
        self.mutex.acquire()
        result = None
        try:
            result = self.dbaccess.execute(raw_sql, params)
        except Exception as e:
            print("db error:", e)
        self.mutex.release()
        return result
