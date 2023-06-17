from app.models.sqlacodegen import *


class MReport(Report):
    """
    可修改配置表
    """
    @staticmethod
    def columns_info():
        """
        表格字段属性
        :return:
        """
        return {
            "section": {
                "title": "节",
                "editmode": 2
            },
            "key": {
                "title": "键",
                "editmode": 2
            },
            "value": {
                "title": "值",
                "editmode": 2
            },
            "description": {
                "title": "描述",
                "editmode": 2
            }
        }

    def dict(self, exclude=None):
        """
        返回一个字典格式
        :return: dict
        """
        entity = self.__dict__
        # 过滤系统内置属性
        del entity['_sa_instance_state']
        if exclude:
            for exc in exclude:
                del entity[exc]
        return entity
