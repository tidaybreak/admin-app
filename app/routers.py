__author__ = 'Ti'

import importlib
from .config import cfg
import os


MOUNT_POINTS = [
]


base_dir = os.path.dirname(os.path.abspath(__file__)) + "/views"
for fn_ in os.listdir(base_dir):
    if fn_.startswith('_'):
        continue
    if fn_.endswith('.py') and not fn_.startswith("_sys_"):
        ext_pos = fn_.rfind('.')
        if ext_pos > 0:
            _name = fn_[:ext_pos]
            if _name != "base":
                module = importlib.import_module("app.views." + _name)
                MOUNT_POINTS.append((module.view, cfg.APPLICATION_ROOT + module.url_prefix))

