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
            "id": {
                "sort": 'custom'
            },
            "date": {
                "sort": 'custom'
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
        entity['importance'] = 1
        if exclude:
            for exc in exclude:
                del entity[exc]
        return entity
