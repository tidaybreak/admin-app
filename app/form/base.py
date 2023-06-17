#coding:utf-8


__author__ = 'Ti'


class BaseModel(object):
    """
    基本流程模型
    """
    def __init__(self, name, display_name):
        """

        """
        self.name = name
        self.display_name = display_name

    def model_attrs(self):
        return {
            "display_name": self.display_name,
            "name": self.name
        }


def get_form(data):
    # 不同操作使用不同form 优先级operate_form form data
    form = None
    operate = data.get("__operate__", "default")
    operate_form = data.get("operate_form", None)
    if operate_form:
        form = operate_form.get(operate, operate_form.get("default", None))
    if form is None:
        form = data.get("form", None)
    if form is None:
        form = data
    return form


class BaseInput(object):
    """
    基本输入框
    """
    def __init__(self, display_name=None, name=None, width=250, is_required=None, is_primary=None, is_unique=None, is_hidden=None, disable_edit=None,
                 is_label=True, is_multi=None, init=None):
        self.type = "input"
        self.lname = display_name
        self.name = name
        self.def_val = None
        # 宽度
        self.width = width
        # 是否必须
        self.is_required = is_required
        # 是否主键
        self.is_primary = is_primary
        # 是否唯一
        self.is_unique = is_unique
        # 是否隐藏
        self.is_hidden = is_hidden
        # 是否不可编辑
        self.disable_edit = disable_edit
        # 是否显示label, table里form不需要显示
        self.is_label = is_label
        # 是否多值
        self.is_multi = is_multi
        # 最大长度
        self.max_size = None
        # ng-init
        self.init = init
        # 占位提示
        self.placeholder = None
        # 字段help
        self.popover = None
        self.table_idx = None
        # 是否可搜索
        self.searchable = True
        self.default = None

    def to_dict(self):
        return {
            "type": self.type,
            "lname": self.lname,
            "name": self.name,
            "def_val": self.def_val,
            "width": self.width,
            "is_required": self.is_required,
            "is_primary": self.is_primary,
            "is_unique": self.is_unique,
            "is_hidden": self.is_hidden,
            "disable_edit": self.disable_edit,
            "is_label": self.is_label,
            "is_multi": self.is_multi,
            "max_size": self.max_size,
            "searchable": self.searchable,
            "init": self.init,
            "placeholder": self.placeholder,
            "popover": self.popover,
            "table_idx": self.table_idx,
            "default": self.default
        }

    def init_input(self, data):
        """
        额外初始化
        :param data:
        :return:
        """

        self.lname = data.get("display_name", None)
        self.name = data.get("name", None)
        self.is_multi = data.get("is_multi", None)
        self.searchable = data.get("searchable", True)
        self.is_required = data.get("is_required", None)
        self.is_primary = data.get("is_primary", None)
        self.is_unique = data.get("is_unique", None)
        self.table_idx = data.get("table_idx", None)

        if self.name is None:
            raise "data:%s" % data

        # 不同操作使用不同form 优先级operate_form form data
        form = get_form(data)

        self.width = form.get("width", 250)
        self.is_hidden = form.get("is_hidden", False)
        self.disable_edit = form.get("disable_edit", None)
        self.is_label = form.get("is_label", True)
        self.max_size = form.get("max_size", None)
        self.init = form.get("init", None)
        self.def_val = form.get("def_val", None)
        self.placeholder = form.get("placeholder", {}) or data.get("placeholder", {}) or "请输入%s" % self.lname
        self.popover = form.get("popover", "")
