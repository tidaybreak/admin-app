__author__ = 'Ti'

import re
import json
from decimal import Decimal
from flask import g
from datetime import datetime, timedelta
from app.services.base import BaseService

TAG = re.compile('[^%]*%([^%]+)%[^%]*')


class OverviewService(BaseService):
    def __init__(self):
        super(OverviewService, self).__init__()

    def update_pue(self, id, value):
        attrs = {
            "id": id,
            "value": value,
            "update_time": datetime.now()
        }
        return self.bulk_update([attrs])
