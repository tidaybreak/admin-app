from app.models.sqlacodegen import *
import copy

class MUser(User):
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
        entity = copy.deepcopy(self.__dict__)
        # 过滤系统内置属性
        if '_sa_instance_state' in entity:
            del entity['_sa_instance_state']

        if exclude:
            for exc in exclude:
                del entity[exc]

        if entity['roleIds']:
            entity['roleIds'] = [int(item) for item in entity['roleIds'].split(',')]
        else:
            entity['roleIds'] = []
        del entity['password']
        return entity
