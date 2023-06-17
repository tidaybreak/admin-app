# coding:utf-8

import os
import traceback
from flask_mail import Mail
from redis import Redis, ConnectionPool
from flask_redis import FlaskRedis
from blinker import Namespace
from redisearch import Client
from flask_caching import Cache
from celery import Celery
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from .loader import load_signals, load_services, load_export, load_form
from influxdb import InfluxDBClient
from app.plugins.csrf_simpe import SimpleCSRFProtect
from app.plugins.supervisor_controller import FlaskSupervisorController
from flask_jwt_extended import JWTManager

DEBUG_TOOL = True
try:
    DEBUG_TOOL = False
    #from flask.ext.debugtool import DebugTool
except ImportError as error:
    print(str(error))
    DEBUG_TOOL = False

__author__ = 'Ti'


class Service(object):
    def __init__(self, app=None):
        self.app = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.load_services()

    def load_services(self):
        """
        """
        services = load_services(self.app)
        for attr, service in list(services.items()):
            self.__dict__[attr.replace('Service', '').lower()] = service()


class Form(object):
    def __init__(self, app=None):
        self.app = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.load_form()

    def load_form(self):
        """
        """
        forms = load_form(self.app)
        for attr, form in list(forms.items()):
            name = attr.replace('InputModel', '')
            if name == "":
                name = "Input"
            self.__dict__[name] = form


class FlaskCelery(Celery):
    def __init__(self, app=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_from_object('app.celeryconfig')
        self.app = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.make_celery(app)

    def make_celery(self, app):
        task_base = self.Task

        class ContextTask(task_base):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return task_base.__call__(self, *args, **kwargs)

        self.Task = ContextTask


class Signal(object):
    def __init__(self, app=None):
        self._signal = Namespace()
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.setup_signal()

    def setup_signal(self):
        executors = load_signals(self.app)
        for key in executors:
            signal_ = self._signal.signal(key)
            signal_.connect(executors[key])
            setattr(self, key, signal_)


class Rdsearch(object):
    def __init__(self, app=None):
        self.app = app
        self.conn = None
        self.rds_index_prefix = None
        if app is not None:
            self.init_app(app)

    def client(self, schema):
        """
        获取客户端
        :param schema:
        :return:
        """
        return Client("%s%s" % (self.rds_index_prefix, schema), conn=self.conn)

    def init_app(self, app):
        self.app = app
        self.setup_rds()

    def setup_rds(self):
        rds_host = self.app.config["RDS_HOST"]
        if rds_host != "":
            self.rds_index_prefix = self.app.config["RDS_INDEX_PRFIX"]
            rds_db = self.app.config["RDS_DB"]
            self.conn = Redis(connection_pool=ConnectionPool(host=rds_host, db=rds_db, port=6379))


class InfluxDB(object):
    def __init__(self, app=None):
        self.app = app
        self.conn = None
        self.rds_index_prefix = None
        if app is not None:
            self.init_app(app)

    def client(self, schema):
        """
        获取客户端
        :param schema:
        :return:
        """
        return Client("%s%s" % (self.rds_index_prefix, schema), conn=self.conn)

    def init_app(self, app):
        self.app = app
        self.setup()

    def setup(self):
        host = self.app.config["INFLUXDB_HOST"]
        user = self.app.config["INFLUXDB_USER"]
        pwd = self.app.config["INFLUXDB_PWD"]
        if host != "":
            self.conn = InfluxDBClient(host, 8086, user, pwd, 'idc')
            self.conn.create_database('idc')


mail = Mail()
db = SQLAlchemy(session_options={"autocommit": False})
influxdb = InfluxDB()
redis = FlaskRedis()
rdsearch = Rdsearch()
celery = FlaskCelery()
serv = Service()
cache = Cache()
form = Form()
signal = Signal()
serv.cache = cache
serv.form = form
serv.celery = celery
serv.signal = signal
session = Session()
sup_ctr = FlaskSupervisorController()

if DEBUG_TOOL:
    debugtool = DebugTool(cache=cache)
else:
    debugtool = None


def init_ext(app):
    """
    这里统一初始化web组件
    :param app:
    :return:
    """
    db.app = app
    db.init_app(app)
    influxdb.init_app(app)
    redis.init_app(app)
    rdsearch.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    celery.init_app(app)
    serv.init_app(app)
    signal.init_app(app)
    form.init_app(app)
    session.init_app(app)
    sup_ctr.init_app(app)
    if DEBUG_TOOL:
        debugtool.app = app
        debugtool.init_app(app)
    app.session_interface.serializer = app.config["SESSION_SERIALIZER"]
    app.permanent_session_lifetime = app.config["SESSION_LIFETIME"]

    # https://blog.csdn.net/weixin_30527875/article/details/114995177
    # sqlalchemy的session是线程平安的，但在多历程环境下，要确保派生子历程时，父历程不存在任何的数据库衔接，能够经由过程挪用db.get_engine(app=app).dispose()来手动烧毁已建立的engine，然后再派生子历程。
    db.get_engine(app=app).dispose()
