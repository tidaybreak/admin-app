# coding:utf-8

import os
import msgpack
from .ext import redis
from datetime import timedelta

__author__ = 'Ti'

basedir = os.path.abspath(os.path.dirname(__file__))
rootdir = os.path.dirname(basedir)


class TraceMixinConfig:
    """
    用来映射trace流程模板中render详细信息的字典，不在这里配置的字典将会默认映射到common
    """

    def __init__(self):
        pass

    pass


class Config(TraceMixinConfig):
    # Flask密钥用于会话 cookie 的安全签名
    SECRET_KEY = os.environ.get('SECRET_KEY') or ''

    APP_NAME = os.getenv('APP_NAME', "app")
    LOG_LEVEL = "INFO"
    APP_BASE_API = '/api/'

    # 解决angular中"{{}}"于Python的flask冲突
    JINJA_OPTIONS = dict(
        variable_start_string='{[',
        variable_end_string=']}'
    )

    # 系统缓存参数
    CACHE_TYPE = "redis"
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 86400)) + 1
    CACHE_KEY_PREFIX = "%s_cache:" % APP_NAME
    CACHE_ENABLE = True

    # SESSION
    SESSION_COOKIE_DOMAIN = os.getenv('SESSION_COOKIE_DOMAIN', "example.com")
    SESSION_TYPE = "redis"
    SESSION_SERIALIZER = msgpack
    SESSION_USE_SIGNER = True
    SESSION_LIFETIME = timedelta(days=7) # minutes=600
    SESSION_KEY_PREFIX = APP_NAME + "SESSION:"
    SESSION_REDIS = redis
    SESSION_COOKIE_PATH = "/"
    APP_KEY_PREFIX = "%s_app:" % APP_NAME

    # 系统MYSQL连接参数
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_RECYCLE = 300
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # es参数
    ES_INDEX = APP_NAME

    # Other
    APPLICATION_ROOT = ""
    UPLOAD_FOLDER = "%s/%s/static" % (basedir, APP_NAME)
    STATIC_FOLDER = "static"
    TEMPLATE_FOLDER = "templates"
    UPLOAD_BASE_FOLDER = os.path.join(basedir, STATIC_FOLDER)
    GLOBAL_TEMP_PATH = "/tmp"

    SUPERVISOR_TEMPLATE_PATH = os.path.join(rootdir, 'supervisord.tpl')
    SUPERVISOR_HTTP_SERVER_ENABLE = True
    SUPERVISOR_HTTP_SERVER_PORT = 9001
    SUPERVISOR_BASIC_AUTH_ENABLE = True
    SUPERVISOR_BASIC_AUTH_USERNAME = "dcim"
    SUPERVISOR_BASIC_AUTH_PASSWORD = "dcim123"
    SUPERVISOR_UNIX_SOCKS_PATH = os.path.join(rootdir, 'supervisor.sock')

    # JSONIFY_MIMETYPE = "application/json;charset=utf-8"
    JSON_AS_ASCII = False


class EnvConfig(Config):
    # 是否开启DEBUG，这里会影响日志的打印
    DEBUG = True
    DEBUG_TB_ENABLED = True
    HTTP_LOGGER_URL = ""

    # view缓存
    CACHE_DEFAULT_TIMEOUT = 0

    # MYSQL数据库链接配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', "mysql+pymysql://user:pass@host:3306/db?charset=utf8")

    # Redis
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/1')
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL', 'redis://redis:6379/1')
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', "redis://redis:6379/5")
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', "redis://redis:6379/5")

    # RediSearch配置 1.2.0只支持在db0上操作
    RDS_HOST = ""

    # ES连接配置
    ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_HOST', "elasticsearch")

    # influxdb
    INFLUXDB_HOST = '172.18.0.145'
    INFLUXDB_USER = 'admin'
    INFLUXDB_PWD = 'admin@123'


env = os.getenv('APP_CONFIG', "Env")
cfg = globals()['%sConfig' % env]
