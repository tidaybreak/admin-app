from datetime import datetime

from app.ext import serv
from .base import *

from flask import request

__author__ = "Ti"

url_prefix = "/api/v1/dashboard"
view_name = os.path.basename(__file__).split('.')[0]
view = Blueprint(view_name, __name__)

@view.route("/electric_cabinet/line_data", methods=["GET"])
def line_data():
    params = request.values
    year = params.get("year", datetime.now().year)
    month = params.get("month")
    data = serv.electriccabinet.line_data(year, month)
    return res_json(code=200, data=data, message="")