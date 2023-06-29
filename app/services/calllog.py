__author__ = 'Ti'

from app.services.base import BaseService
from passlib.hash import pbkdf2_sha256 as sha256
from app.utils.utils import str2md5
from flask import session


class CalllogService(BaseService):
    def __init__(self):
        super(CalllogService, self).__init__()

    def pages(self, query_dict, page=1, limit=None):
        # print(session.get(b'user')['dataScope'])
        # query_dict = {
        #     "filter": {
        #         "and": {
        #             "status": "date",
        #             "age": {
        #                 "gt": startTime,
        #                 "lte": endTime
        #             }
        #         }
        #     }
        # }
        data = super().fetch_list(query_dict=query_dict, page=page, limit=limit, to_type="dict", field_info=True)
        return data
