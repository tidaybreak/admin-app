# coding:utf-8

import os
import imp
import traceback

__author__ = 'Ti'


def load_plugins(name, app):
    """
    加载模块
    @param name string:插件相对plugins的命名空间
    @return dict:
    """
    names = {}
    modules = []
    funcs = {}
    name = name.replace('.', '/')
    base_dir = os.path.dirname(os.path.abspath(__file__))
    mod_dirs = [os.path.join(base_dir, "plugins", name)]
    for mod_dir in mod_dirs:
        if not os.path.isdir(mod_dir):
            continue
        for fn_ in os.listdir(mod_dir):
            if fn_.startswith('_'):
                continue
            if fn_.endswith('.py') and not fn_.startswith("_sys_"):
                extpos = fn_.rfind('.')
                if extpos > 0:
                    _name = fn_[:extpos]
                else:
                    _name = fn_
                names[_name] = os.path.join(mod_dir, fn_)
    for name in names:
        try:
            # 模块的加载mod_dirs一定是一个list类型数据，否则执行失败
            fn_, path, desc = imp.find_module(name, mod_dirs)
            mod = imp.load_module(name, fn_, path, desc)
        except:
            print((traceback.format_exc()))
            continue
        modules.append(mod)
    for mod in modules:
        for attr in dir(mod):
            if attr.startswith('_'):
                continue
                # 将加载的模块存放到字典里面
            if callable(getattr(mod, attr)):
                func = getattr(mod, attr)
                # 不加flask上下文这里执行不了
                with app.app_context():
                    try:
                        # TODO mod=request 会出错 有空查下
                        if not getattr(func, "export", False):
                            continue

                        funcs[func.__name__] = func
                    except:
                        #print traceback.format_exc()
                        continue
    return funcs


def load_selfs(path, app):
    """
    加载模块
    @param name string:插件相对plugins的命名空间
    @return dict:
    """
    names = {}
    modules = []
    funcs = {}
    # name = name.replace('.', '/')
    base_dir = os.path.dirname(os.path.abspath(__file__))
    mod_dir = os.path.join(base_dir, path)
    for fn_ in os.listdir(mod_dir):
        if fn_.startswith('_'):
            continue
        if fn_.endswith('.py') and not fn_.startswith("_sys_"):
            extpos = fn_.rfind('.')
            if extpos > 0:
                _name = fn_[:extpos]
            else:
                _name = fn_
            names[_name] = os.path.join(mod_dir, fn_)
    for name in names:
        try:
            # 模块的加载mod_dirs一定是一个list类型数据，否则执行失败
            fn_, path, desc = imp.find_module(name, [mod_dir])
            mod = imp.load_module(name, fn_, path, desc)
        except:
            print((traceback.format_exc()))
            continue
        modules.append(mod)
    for mod in modules:
        for attr in dir(mod):
            if attr.startswith('_'):
                continue
                # 将加载的模块存放到字典里面
            if callable(getattr(mod, attr)):
                func = getattr(mod, attr)
                # 不加flask上下文这里执行不了
                with app.app_context():
                    try:
                        # TODO mod=request 会出错 有空查下
                        if not getattr(func, "export", False):
                            continue

                        funcs[func.__name__] = func
                    except:
                        #print traceback.format_exc()
                        continue
    return funcs


def load_signals(app):
    """
    加载信号处理器
    @param name string:插件相对signals的命名空间
    @return dict:
    """
    names = {}
    modules = []
    funcs = {}
    base_dir = os.path.dirname(os.path.abspath(__file__))
    mod_dirs = [os.path.join(base_dir, "signals")]
    for mod_dir in mod_dirs:
        if not os.path.isdir(mod_dir):
            continue
        for fn_ in os.listdir(mod_dir):
            if fn_.startswith('_'):
                continue
            if fn_.endswith('.py') and not fn_.startswith("_sys_"):
                extpos = fn_.rfind('.')
                if extpos > 0:
                    _name = fn_[:extpos]
                else:
                    _name = fn_
                names[_name] = os.path.join(mod_dir, fn_)
    for name in names:
        try:
            # 模块的加载mod_dirs一定是一个list类型数据，否则执行失败
            fn_, path, desc = imp.find_module(name, mod_dirs)
            mod = imp.load_module(name, fn_, path, desc)
        except:
            print((traceback.format_exc()))
            continue
        modules.append(mod)
    for mod in modules:
        for attr in dir(mod):
            if attr.startswith('_'):
                continue
                # 将加载的模块存放到字典里面
            if callable(getattr(mod, attr)):
                func = getattr(mod, attr)
                # 不加flask上下文这里执行不了
                with app.app_context():
                    if not getattr(func, "export", False):
                        continue
                    try:
                        funcs[func.__name__] = func
                    except:
                        print((traceback.format_exc()))
                        continue
    return funcs


def load_services(app):
    """
    加载service
    @param name string:插件相对services的命名空间
    @return dict:
    """
    names = {}
    modules = []
    funcs = {}
    base_dir = os.path.dirname(os.path.abspath(__file__))
    mod_dirs = [os.path.join(base_dir, "services")]
    for mod_dir in mod_dirs:
        if not os.path.isdir(mod_dir):
            continue
        for fn_ in os.listdir(mod_dir):
            if fn_.startswith('_'):
                continue
            if fn_.endswith('.py') and not fn_.startswith("_sys_"):
                extpos = fn_.rfind('.')
                if extpos > 0:
                    _name = fn_[:extpos]
                else:
                    _name = fn_
                names[_name] = os.path.join(mod_dir, fn_)
    for name in names:
        try:
            # 模块的加载mod_dirs一定是一个list类型数据，否则执行失败
            fn_, path, desc = imp.find_module(name, mod_dirs)
            mod = imp.load_module(name, fn_, path, desc)
        except:
            print((traceback.format_exc()))
            continue
        modules.append(mod)
    for mod in modules:
        for attr in dir(mod):
            if attr.startswith('_'):
                continue
                # 将加载的模块存放到字典里面
            if callable(getattr(mod, attr)):
                obj = getattr(mod, attr)
                # 不加flask上下文这里执行不了
                with app.app_context():
                    if not attr.endswith('Service') or attr == "BaseService":
                        continue
                    try:
                        funcs[attr] = obj
                    except:
                        print((traceback.format_exc()))
                        continue
    return funcs


def load_export(app):
    """
    加载service
    @param name string:插件相对export的命名空间
    @return dict:
    """
    names = {}
    modules = []
    funcs = {}
    base_dir = os.path.dirname(os.path.abspath(__file__))
    mod_dirs = [os.path.join(base_dir, "export")]
    for mod_dir in mod_dirs:
        if not os.path.isdir(mod_dir):
            continue
        for fn_ in os.listdir(mod_dir):
            if fn_.startswith('_'):
                continue
            if fn_.endswith('.py') and not fn_.startswith("_sys_"):
                extpos = fn_.rfind('.')
                if extpos > 0:
                    _name = fn_[:extpos]
                else:
                    _name = fn_
                names[_name] = os.path.join(mod_dir, fn_)
    for name in names:
        try:
            # 模块的加载mod_dirs一定是一个list类型数据，否则执行失败
            fn_, path, desc = imp.find_module(name, mod_dirs)
            mod = imp.load_module(name, fn_, path, desc)
        except:
            print((traceback.format_exc()))
            continue
        modules.append(mod)
    for mod in modules:
        for attr in dir(mod):
            if attr.startswith('_'):
                continue
                # 将加载的模块存放到字典里面
            if callable(getattr(mod, attr)):
                obj = getattr(mod, attr)
                # 不加flask上下文这里执行不了
                with app.app_context():
                    if not attr.endswith('Export') or attr == "BaseExport":
                        continue
                    try:
                        funcs[attr] = obj
                    except:
                        print((traceback.format_exc()))
                        continue
    return funcs


def load_form(app):
    """
    加载form
    @return dict:
    """
    names = {}
    modules = []
    funcs = {}
    base_dir = os.path.dirname(os.path.abspath(__file__))
    mod_dirs = [os.path.join(base_dir, "form")]
    for mod_dir in mod_dirs:
        if not os.path.isdir(mod_dir):
            continue
        for fn_ in os.listdir(mod_dir):
            if fn_.startswith('_'):
                continue
            if fn_.endswith('.py') and not fn_.startswith("_sys_"):
                extpos = fn_.rfind('.')
                if extpos > 0:
                    _name = fn_[:extpos]
                else:
                    _name = fn_
                names[_name] = os.path.join(mod_dir, fn_)
    for name in names:
        try:
            # 模块的加载mod_dirs一定是一个list类型数据，否则执行失败
            fn_, path, desc = imp.find_module(name, mod_dirs)
            mod = imp.load_module(name, fn_, path, desc)
        except:
            print((traceback.format_exc()))
            continue
        modules.append(mod)
    for mod in modules:
        for attr in dir(mod):
            if attr.startswith('_'):
                continue
                # 将加载的模块存放到字典里面
            if callable(getattr(mod, attr)):
                obj = getattr(mod, attr)
                # 不加flask上下文这里执行不了
                with app.app_context():
                    if not attr.endswith('InputModel') or attr == "BaseInput":
                        continue
                    try:
                        funcs[attr] = obj
                    except:
                        print((traceback.format_exc()))
                        continue
    return funcs
