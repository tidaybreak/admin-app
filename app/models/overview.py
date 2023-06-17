from app.models.sqlacodegen import *


class MOverview(Overview):
    """
    机房表
    """
    @staticmethod
    def columns_info():
        """
        表格字段属性
        :return:
        """
        return {
            "id": {
                "title": "机房编号",
                "sortable": True,
                "align": "center",
                "width": 100,
                "display": True
            },
            "name": {
                "title": "机房名称",
                "sortable": True,
                "display": True,
                "searchable": True,
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
        entity["update_time"] = entity["update_time"].strftime("%Y-%m-%d")
        return entity
