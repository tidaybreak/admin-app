from app.models.sqlacodegen import *
import copy

class MDept(Dept):
    """
    可修改配置表
    """
    @staticmethod
    def columns_info():
        """
        表格字段属性
        :return:
        """
        return {}

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
        if entity['parentId'] != entity['id']:
            entity['treePath'] = str(entity['parentId']) + ',' + str(entity['id'])
        else:
            entity['treePath'] = str(entity['id'])
        return entity
