from app.models.sqlacodegen import *
import copy
from app.utils.utils import set_form_value
from app.ext import serv


class MBusDialtask(BusDialtask):
    """
    可修改配置表
    """
    @staticmethod
    def columns_info():
        """
        表格字段属性
        :return:

            "user_name": {
                "type": "SELECT",
                "type_data": {
                    "trigger": "__uid__",   // 二级select 触发字段 为空标识一级select
                    "type": "ciopass_user", // select 查询标识
                    "data": []
                }
            }
        """
        data = {
            "percentage": {
                "title": '预测式倍率'
            },
            "task_type": {
                "title": '任务类型'
            },
            "ai_distribution_type": {
                "title": '预览式'
            },
            "status": {
                "title": '外呼状态',
                "type": "SELECT",
                "type_data": {
                    "type": "",
                    "data": [
                        {"val": "", "label": "所有"},
                        {"val": "发送中", "label": "发送中"},
                        {"val": "已发送", "label": "已发送"},
                        {"val": "暂停发送", "label": "暂停发送"}
                    ]
                }
            },
            "__uid__": {
                "title": '主账号',
                "type": "SELECT",
                "type_data": {
                    "type": "username",
                    "data": []
                }
            },
            "project_caption": {
                "type": "SELECT",
                "type_data": {
                    "trigger": "__uid__",
                    "type": "templatelist",
                    "data": []
                }
            },
            "user_name": {
                "type": "SELECT",
                "type_data": {
                    "trigger": "__uid__",
                    "type": "ciopass_user",
                    "data": []
                }
            },
            "tels": {
                "type": "UPLOAD",
                "form_type": "upload",
                "title": "号码"
            },
            "tels_amount": {
                "type": "INTEGER",
                "title": "号码数量",
                "type_data": {
                    "max": 100000
                }
            }
        }

        data = set_form_value(data, 'edit', 1, ['__uid__', 'source', 'project_caption', 'user_name', 'tels', 'tels_amount'])
        data = set_form_value(data, 'sort', 1, ['total_count', 'send_count', 'unsend_count', 'success', 'fail'])
        data = set_form_value(data, 'search', 1, ['__uid__', 'user_name', 'status', 'created_at', 'project_caption'])
        data = set_form_value(data, 'show', 0, ['tels', 'dial_task_main_sn', 'user_sn', 'last_modify', 'started_at', 'stopped_at', 'create_time', 'percentage', 'ai_distribution_type', 'project_sn'])
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

        if entity['__uid__']:
            entity['__uid__'] = serv.user.username(entity['__uid__'])
        return entity
