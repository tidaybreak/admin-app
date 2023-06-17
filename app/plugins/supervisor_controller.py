import warnings

import socket
from xmlrpc.client import Transport, ServerProxy
from http.client import HTTPConnection

class UnixStreamHTTPConnection(HTTPConnection):
    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.host)

class UnixStreamTransport(Transport, object):
    def __init__(self, socket_path):
        self.socket_path = socket_path
        super(UnixStreamTransport, self).__init__()

    def make_connection(self, host):
        return UnixStreamHTTPConnection(self.socket_path)

class FlaskSupervisorController(object):
    def __init__(self, app=None):
        self.app = None
        self.uri = None
        self.sup_cfg = {}
        self.socks = None
        self.server = None
        self.supervisor = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.uri = None
        self.sup_cfg = {key: value for key, value in app.config.items() if key.startswith("SUPERVISOR")}
        self.socks = self.sup_cfg.get("SUPERVISOR_UNIX_SOCKS_PATH")
        if self.socks is None:
            warnings.warn(
                "缺少SUPERVISOR_UNIX_SOCKS_PATH配置将无法远程控制supervisord"
            )
        self.server = ServerProxy('http://localhost', transport=UnixStreamTransport(self.socks))
        self.supervisor = self.server.supervisor

    def __getattr__(self, name):
        return getattr(self.supervisor, name)
