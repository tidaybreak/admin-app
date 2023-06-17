__author__ = 'Ti'

import os
from app.ext import db
# from .electric import *

base_dir = os.path.dirname(os.path.abspath(__file__))
for fn_ in os.listdir(base_dir):
    if fn_.startswith('_'):
        continue
    if fn_.endswith('.py') and not fn_.startswith("_sys_"):
        ext_pos = fn_.rfind('.')
        if ext_pos > 0:
            _name = fn_[:ext_pos]
            if _name != "sqlacodegen":
                exec("from ." + _name + " import *")

