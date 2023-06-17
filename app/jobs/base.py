import traceback

from app.ext import celery


def async_task(*args, **kwargs):
    def wrap(func):
        if "name" in kwargs:
            del kwargs["name"]
        name = func.__name__
        @celery.task(name=name, *args, **kwargs)
        def wrapper(*w_args, **w_kwagrs):
            try:
                print("任务[{task_name}]启动".format(task_name=name))
                ok, msg = func(*w_args, **w_kwagrs)
                print("任务[{task_name}]完成".format(task_name=name))
                return ok, msg
            except Exception as e:
                error_msg = traceback.format_exc()
                print("任务[{task_name}]发生错误, 错误信息:\n {error_msg}".format(task_name=name, error_msg=error_msg))
                return False,  str(e)
        return wrapper
    return wrap
