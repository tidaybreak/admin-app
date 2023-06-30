from app.models.sqlacodegen import *
import copy


class MCalllog(BusCalllog):
    """
    可修改配置表
    """
    @staticmethod
    def columns_info():
        """
        表格字段属性
        :return:
        """
        search_able = ['phone', 'source', 'started_at', 'talktimes', 'status', 'status_manual', 'operator', 'user_name', 'team_name', 'mark', 'download_time']

        data = {
            "__uid__": {
                "show": 0
            },
            "sn": {
                "show": 0,
                "edit": 0
            },
            "mark": {
                "edit": 1
            },
            "update_time": {
                "show": 0
            },
            "create_time": {
                "title": '获取时间'
            }
        }
        for ent in search_able:
            if ent in data:
                data[ent]['search'] = 1
            else:
                data[ent] = {
                    "search": 1
                }
        return data

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
