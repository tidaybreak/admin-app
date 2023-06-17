# coding=utf-8

import json
import sys
import time
import logging
import traceback
from flask import Flask
from requests import session as Session
from .ext import init_ext
from datetime import datetime, date

__author__ = 'Ti'


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        # sqlalchemy type
        if hasattr(o, '__visit_name__'):
            return o.__visit_name__
        if isinstance(o, date):
            return o.strftime("%Y-%m-%d")
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        return json.JSONEncoder.default(self, o)


def create_app(conf=None):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(conf.JINJA_OPTIONS)
    Flask.jinja_options = jinja_options

    app = Flask("app")
    app.json_encoder = JSONEncoder
    if conf:
        app.config.from_object(conf)

    init_ext(app)
    configure_logging(app)
    return app


def configure_blueprints(app, modules):
    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix=url_prefix)
    return app


def configure_logging(app):
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(pathname)s %(lineno)d - %(message)s")
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))

    formatter = logging.Formatter(
        '{"level": "%(levelname)s", "create_time": "%(asctime)s", "text": "%(pathname)s %(lineno)d - %(message)s"}')
    app_name = app.config['APP_NAME']
    logger_url = app.config['HTTP_LOGGER_URL']
    http_handler = HTTPHandler(url=logger_url, app_name=app_name)
    http_handler.setFormatter(formatter)
    http_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))

    app.logger.addHandler(console_handler)
    app.logger.addHandler(http_handler)
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))


session = Session()


class HTTPHandler(logging.Handler):
    def __init__(self, url, app_name):
        logging.Handler.__init__(self)
        self.url = url
        self.app_name = app_name

    def get_full_message(self, record):
        if record.exc_info:
            return '\n'.join(traceback.format_exception(*record.exc_info))
        else:
            return record.getMessage()

    def emit(self, record):
        try:
            log = self.format(record)
            try:
                payload = json.loads(log)
            except:
                print(log)
                return
            if len(self.url) > 0:
                payload["app"] = self.app_name
                # change '2017-11-02 19:12:34,817' == > 2017-11-02 19:12:34
                now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                payload["create_time"] = payload.get("create_time", now).split(",")[0]
                res = session.post(self.url, data=json.dumps(payload))
                data = res.json()
                if not data["success"]:
                    self.handleError(record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
