from app.models.sqlacodegen import *
import copy


class MCalllog(Calllog):
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
            "sn": {
                "show": 0
            }
        }

    def dict(self, exclude=None):
        """
        返回一个字典格式
        :return: dict
        """
        entity = copy.deepcopy(self.__dict__)
        # 过滤系统内置属性
        if '_sa_instance_state' in entity:
            del entity['_sa_instance_state']

        if exclude:
            for exc in exclude:
                del entity[exc]
        # if entity['perms']:
        #     entity['perms'] = entity['perms'].split(',')
        # else:
        #     entity['perms'] = []

        return entity