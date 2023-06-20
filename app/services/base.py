__author__ = 'Ti'

import os
import threading
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
        self.columns = reflection.Inspector.from_engine(engine).get_columns(table_name)
        for idx, val in enumerate(self.columns):
            self.columns[idx]['id'] = idx
            if val['name'] in columns_info:
                self.columns[idx] = {**self.columns[idx], **columns_info[val['name']]}

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

    def find_one(self, query, to_dict=False):
        query_dict = {
            "filter": query
        }
        items = self.fetch_list(query_dict=query_dict, to_dict=to_dict)["items"]
        if len(items) > 0:
            return items[0]
        else:
            return None

    def delete(self, id):
        return self.dbaccess.delete(self.model_name, id)

    def update(self, query_dict={}, update_dict={}, insert=False):
        return self.dbaccess.update(self.model_name, query_dict, update_dict, insert=insert)

    def fetch_list(self, page=1, limit=None, query_dict={}, to_dict=True):
        """
        获取分页数据
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
        :param to_dict:
        :return:
        """
        result = []
        #print("mutex-acquire  %s %s  %s  %s  %s" % (os.getpid(), pid, t.ident, t.getName(), self.mutex))
        entities = []
        total = -1
        try:
            query = self.dbaccess.elastic_query(self.model(), query_dict)
            total = query.count()

            if limit is not None:
                query = query.offset((page - 1) * limit).limit(limit)
            entities = query.all()
        except Exception as e:
            #print("db error:", e)
            raise e

        for entity in entities:
            if to_dict:
                result.append(entity.dict())
            else:
                result.append(entity)
        data = {
            "total": total,
            "items": result,
            "columns": self.columns
        }
        return data

    def bulk_save(self, conds):
        self.mutex.acquire()
        result = None
        try:
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
        self.mutex.acquire()
        result = None
        try:
            result = self.dbaccess.execute(raw_sql, params)
        except Exception as e:
            print("db error:", e)
        self.mutex.release()
        return result
