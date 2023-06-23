import os

from app.config import cfg

from celery.schedules import crontab
from celery import signature
# kombu 版本要从 4.6.5 降级到 4.6.4 不然无法路由消息到交换机
from kombu import Exchange, Queue, binding

"""
Exchanges, queues, and routing keys
1.Messages are sent to exchanges.
2.An exchange routes messages to one or more queues. Several exchange types exists, providing different ways to do 
routing, or implementing different messaging scenarios.
3.The message waits in the queue until someone consumes it.
4.The message is deleted from the queue when it has been acknowledged.
"""


exchange_list = Exchange(cfg.APP_NAME, type="direct")

task_queues = (
    Queue("default", Exchange("default"), routing_key="default"),
    Queue(cfg.APP_NAME, []),
)

# task 不能写exchange: xxx 不然worker接收不到任务
task_routes = {
    # "import_electric_cabinet_beat": {
    #     "queue": cfg.APP_NAME,
    #     "routing_key": "electric_cabinet.import_beat"
    # }
}

# 默认为celery
task_default_queue = cfg.APP_NAME
task_default_exchange = cfg.APP_NAME
task_default_routing_key = cfg.APP_NAME

# 序列化器
task_serializer = "pickle"
accept_content = ["pickle", "json", "msgpack", "yaml"]
imports = [
    "app.jobs.telad"
]
timezone = "Asia/Shanghai"
# 报告STARTED状态
task_track_started = True
# 工作进程数量 io操作可以适量提高 受CPU数量限制
worker_concurrency = 5
# 单个worker执行最多N次任务后被回收 * 防止内存泄露
worker_max_tasks_per_child = 2
# 等待新的worker的启动时间
worker_proc_alive_timeout = 15

beat_schedule = {
    "报表": {
        "task": "app.jobs.telad.crm_list",
        "schedule": crontab(minute="*/1"),
        "options": {
            "queue": "default",
            "link": signature(
                "app.jobs.telad.crm_list_signature"
            )
        }
    }
}
#"schedule": crontab(minute="40", hour="1"),

broker_url = cfg.CELERY_BROKER_URL                     # os.environ.get("BROKER_URL", "redis://redis-dev.ofidc.com:6379/5")
result_backend = cfg.CELERY_RESULT_BACKEND      # os.environ.get("CELERY_RESULT_BACKEND", "redis://redis-dev.ofidc.com:6379/5")

