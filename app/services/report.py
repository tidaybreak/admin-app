__author__ = 'Ti'


from app.services.base import BaseService
from passlib.hash import pbkdf2_sha256 as sha256
from app.utils.utils import str2md5


class ReportService(BaseService):
    def __init__(self):
        super(ReportService, self).__init__()

    def get_report(self, page=1, limit=None):
        query_dict = {
            "filter": {
            }
        }
        data = super().fetch_list(query_dict=query_dict, page=page, limit=limit, to_dict=True)
        return data
