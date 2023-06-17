from flask import request, current_app, abort, Blueprint
import sys

PY2 = sys.version_info[0] == 2
if not PY2:
    text_type = str
    string_types = (str,)
else:
    text_type = unicode
    string_types = (str, unicode)

class SimpleCSRFProtect(object):
    def __init__(self, app=None):
        self._exempt_views = set()
        self._exempt_blueprints = set()
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.extensions["simple_csrf"] = self
        app.config.setdefault("SIMPLE_CSRF_ENABLED", True)
        app.config["SIMPLE_CSRF_METHODS"] = set(app.config.get(
            "SIMPLE_CSRF_METHODS", ["POST", "PUT", "PATCH", "DELETE"]
        ))
        app.config.setdefault(
            "SIMPLE_CSRF_HEADER", "X-CSRF-Token"
        )
        app.config.setdefault(
            "SIMPLE_CSRF_FIELD", "csrf_token"
        )
        app.config.setdefault(
            "SIMPLE_CSRF_QUERY", "csrf_token"
        )
        app.config.setdefault(
            "SIMPLE_CSRF_TOKEN", None
        )
        app.config.setdefault(
            "SIMPLE_CSRF_TOKEN_FUNC", lambda: "2bbb76954d739ea67ef3e80da34c15bd5a9cfb69"
        )
        app.config.setdefault(
            "SIMPLE_CSRF_VERIFY_IP", []
        )

        @app.before_request
        def csrf_protect():
            if not app.config["SIMPLE_CSRF_ENABLED"]:
                return

            if app.config["SIMPLE_CSRF_VERIFY_IP"] and request.remote_addr not in app.config["SIMPLE_CSRF_VERIFY_IP"]:
                return

            view = app.view_functions.get(request.endpoint)

            if not view:
                return

            if request.blueprint in self._exempt_blueprints:
                return

            dest = '%s.%s' % (view.__module__, view.__name__)

            if dest in self._exempt_views:
                return

            self.protect()

    def protect(self):
        if request.method not in current_app.config["SIMPLE_CSRF_METHODS"]:
            return

        field_name = current_app.config["SIMPLE_CSRF_FIELD"]
        header_name = current_app.config["SIMPLE_CSRF_HEADER"]
        query_name = current_app.config["SIMPLE_CSRF_QUERY"]
        csrf_token = request.form.get(field_name) or request.headers.get(header_name) or request.values.get(query_name)

        token = current_app.config["SIMPLE_CSRF_TOKEN"]
        token_func = current_app.config["SIMPLE_CSRF_TOKEN_FUNC"]
        if token_func:
            token = token_func()

        if csrf_token == token:
            return
        else:
            abort(400)

    def exempt(self, view):
        if isinstance(view, Blueprint):
            self._exempt_blueprints.add(view.name)
            return view

        if isinstance(view, string_types):
            view_location = view
        else:
            view_location = '%s.%s' % (view.__module__, view.__name__)

        self._exempt_views.add(view_location)
        return view