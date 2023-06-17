# coding:utf-8

from flask import current_app
import app.ext
import yaml
import json

from app.form.base import BaseModel, BaseInput, get_form


__author__ = 'Ti'


class FormModel(BaseModel):
    """
    """

    def __init__(self, name, display_name):
        super(FormModel, self).__init__(name, display_name)
        self.init = None
        self.object = None
        self.inputs = {}

    def add_obj(self, tag, obj):
        """

        """
        if not tag:
            sort = 0
            tag_name = "基本信息"
        else:
            try:
                j_tag = json.loads(tag)
                sort = j_tag[0]
                tag_name = j_tag[1]
            except ValueError as e:
                sort = 99
                tag_name = tag

        if tag_name in self.inputs:
            self.inputs[tag_name]["inputs"].append(obj)
        else:
            self.inputs[tag_name] = {"sort": sort, "inputs": []}
            self.inputs[tag_name]["inputs"] = [obj]

    def to_dict(self):
        return {
            "name": self.name,
            "display_name": self.display_name,
            "init": self.init,
            "object": self.object,
            "inputs": self.inputs
        }

    def __repr__(self):
        return "<FormModel (name=%s)>" % self.name


class OperateFormModel(BaseModel):
    """
    """

    def __init__(self, name, display_name=None):
        super(OperateFormModel, self).__init__(name, display_name)
        self.init = None
        self.object = None
        self.inputs = {}

    def add_obj(self, name, display_name, obj=None, description=None):
        """

        """
        if "items" in self.inputs:
            self.inputs["items"].append(obj)
        else:
            if obj is None:
                items = []
            else:
                items = [obj]
            self.inputs = {"display_name": display_name, "name": name, "items": items, "desc": description}

    def to_dict(self):
        return {
            "name": self.name,
            "display_name": self.display_name,
            "init": self.init,
            "object": self.object,
            "inputs": self.inputs
        }

    def __repr__(self):
        return "<FormModel (name=%s)>" % self.name


class InputModel(BaseInput):
    def __init__(self):
        super(InputModel, self).__init__()
        self.type = "Input"
        self.input_type = "String"
        self.size = None

    def init_input(self, data):
        """
        额外初始化
        :param data:
        :return:
        """
        super(InputModel, self).init_input(data)
        self.input_type = data.get("type", "String")

        def_val = get_form(data).get("def_val")
        if def_val:
            if self.input_type == 'Integer':
                self.def_val = int(def_val)
            elif self.input_type == 'Float':
                self.def_val = float(def_val)
            else:
                self.def_val = "'%s'" % def_val

        self.size = data.get("size", 1000)

    def to_dict(self):
        base_dict = super(InputModel, self).to_dict()
        base_dict.update(
            {
                "size": self.size,
                "input_type": self.input_type
            }
        )
        return base_dict


class TextareaInputModel(BaseInput):
    def __init__(self):
        super(TextareaInputModel, self).__init__()
        self.type = "Textarea"
        self.cols = None
        self.rows = None

    def init_input(self, data):
        """
        额外初始化
        :param data:
        :return:
        """
        super(TextareaInputModel, self).init_input(data)

        self.rows = get_form(data).get("rows")
        self.cols = get_form(data).get("cols")

    def to_dict(self):
        base_dict = super(TextareaInputModel, self).to_dict()
        base_dict.update(
            {
                "cols": self.cols,
                "rows": self.rows
            }
        )
        return base_dict


class UeditorInputModel(BaseInput):
    def __init__(self):
        super(UeditorInputModel, self).__init__()
        self.type = "Ueditor"
        self.cols = None
        self.rows = None

    def init_input(self, data):
        """
        额外初始化
        :param data:
        :return:
        """
        super(UeditorInputModel, self).init_input(data)
        self.rows = get_form(data).get("rows")
        self.cols = get_form(data).get("cols")

    def to_dict(self):
        base_dict = super(UeditorInputModel, self).to_dict()
        base_dict.update(
            {
                "cols": self.cols,
                "rows": self.rows
            }
        )
        return base_dict


class TableInputModel(BaseInput):
    def __init__(self):
        super(TableInputModel, self).__init__()
        self.type = "Table"
        self.size = None
        self.form = None
        self.front_input = {}

    def init_input(self, data):
        """
        额外初始化
        :param data:
        :return:
        """
        super(TableInputModel, self).init_input(data)
        input_form = yaml.load(data["table_input_form"])
        form = parse_operate_form(self.name, input_form or {}, self.lname, "description")
        for key, value in data.items():
            if key.startswith("table_front_input"):
                self.front_input[key] = value
        if data.get("table_front_input_value_format") == "Object":
            self.front_input["table_front_input_value_object_display_key"] = data.get("table_front_input_value_object_display_key", "display")
            self.front_input["table_front_input_value_object_value_key"] = data.get("table_front_input_value_object_value_key", "value")
        self.form = form.to_dict()

    def to_dict(self):
        base_dict = super(TableInputModel, self).to_dict()
        base_dict.update(
            {
                "size": self.size,
                "front_input": self.front_input,
                "form": self.form
            }
        )
        return base_dict


class NormalFileInputModel(BaseInput):
    def __init__(self):
        super(NormalFileInputModel, self).__init__()
        self.type = "NormalFile"
        self.size = None
        self.upload_addr = None

    def init_input(self, data):
        """
        额外初始化
        :param data:
        :return:
        """
        super(NormalFileInputModel, self).init_input(data)
        self.upload_addr = data["upload_addr"]
        self.width = 80

    def to_dict(self):
        base_dict = super(NormalFileInputModel, self).to_dict()
        base_dict.update(
            {
                "size": self.size,
                "upload_addr": self.upload_addr
            }
        )
        return base_dict


class UploadFileInputModel(BaseInput):
    def __init__(self):
        super(UploadFileInputModel, self).__init__()
        self.type = "UploadFile"
        self.file_type = []

    def init_input(self, data):
        """
        额外初始化
        :param data:
        :return:
        """
        super(UploadFileInputModel, self).init_input(data)
        self.file_type = data.get("file_type", [])
        self.width = 80

    def to_dict(self):
        base_dict = super(UploadFileInputModel, self).to_dict()
        base_dict.update(
            {
                "file_type": self.file_type
            }
        )
        return base_dict


class DateInputModel(BaseInput):
    def __init__(self):
        super(DateInputModel, self).__init__()
        self.type = "Date"
        self.size = None
        self.format = None
        self.minview = None

    def init_input(self, data):
        """
        额外初始化
        :param data:
        :return:
        """
        super(DateInputModel, self).init_input(data)
        self.format = get_form(data).get("format")    # yyyy-mm-dd hh:ii:ss
        self.minview = get_form(data).get("minview", 0)   # 0:min 1: hour 2:day 3:month

    def to_dict(self):
        base_dict = super(DateInputModel, self).to_dict()
        base_dict.update(
            {
                "size": self.size,
                "format": self.format,
                "minview": self.minview
            }
        )
        return base_dict


class ReferenceInputModel(BaseInput):
    def __init__(self):
        super(ReferenceInputModel, self).__init__()
        self.type = "Reference"
        self.size = None
        self.is_can_add = None
        self.reference_formatter = None
        self.schema = None

    def init_input(self, data):
        """
        额外初始化
        :param data:
        :return:
        """
        super(ReferenceInputModel, self).init_input(data)
        self.is_multi = data["is_multi"]
        self.reference_formatter = data["reference_formatter"] or ''
        self.schema = data["reference"]
        self.schema_var = data.get("reference_var", False)

    def to_dict(self):
        base_dict = super(ReferenceInputModel, self).to_dict()
        base_dict.update(
            {
                "size": self.size,
                "is_can_add": self.is_can_add,
                "schema": self.schema,
                "schema_var": self.schema_var,
                "reference_formatter": self.reference_formatter
            }
        )
        return base_dict


class RadioInputModel(BaseInput):
    def __init__(self):
        super(RadioInputModel, self).__init__()
        self.type = "Radio"
        self.value = None

    def init_input(self, data):
        """
        额外初始化
        :param data:
        :return:
        """
        super(RadioInputModel, self).init_input(data)
        self.value = get_form(data).get("value")
        if not self.value:
            self.value = ','.join(data["enum_item"])

    def to_dict(self):
        base_dict = super(RadioInputModel, self).to_dict()
        base_dict.update(
            {
                "value": self.value
            }
        )
        return base_dict


class DropDownInputModel(BaseInput):
    def __init__(self):
        super(DropDownInputModel, self).__init__()
        self.type = "DropDown"
        self.value = None
        self.is_can_add = None

    def init_input(self, data):
        """
        额外初始化
        :param data:
        :return:
        """
        super(DropDownInputModel, self).init_input(data)
        if data["type"] == "Enum":
            self.value = ','.join(data["enum_item"])
        else:
            self.value = get_form(data).get("value", "")
        self.is_can_add = get_form(data).get("is_can_add", None)

    def to_dict(self):
        base_dict = super(DropDownInputModel, self).to_dict()
        base_dict.update(
            {
                "value": self.value,
                "is_can_add": self.is_can_add,
            }
        )
        return base_dict


class MultiDropInputModel(BaseInput):
    def __init__(self, data_source=None):
        super(MultiDropInputModel, self).__init__()
        self.type = "MultiDrop"
        self.value = None
        self.is_can_add = None
        self.data_source = data_source

    def init_input(self, data):
        """
        额外初始化
        :param data:
        :return:
        """
        super(MultiDropInputModel, self).init_input(data)
        self.is_can_add = get_form(data).get("is_can_add", None)

    def to_dict(self):
        base_dict = super(MultiDropInputModel, self).to_dict()
        base_dict.update(
            {
                "value": self.value,
                "is_can_add": self.is_can_add
            }
        )
        return base_dict


def make_operate_form(data):
    """
    生成form的json结构
    :param entity:
    :return:
    """
    if data.get("is_multi") is None:
        data["is_multi"] = False

    if data.get("is_required") is None:
        data["is_required"] = False

    if data["type"] == "Reference":
        type_ = "Reference"
    elif data["type"] == "Enum":
        type_ = "DropDown"
    elif data["type"] == "Radio":
        type_ = "Radio"
    elif data["type"] == "Date":
        type_ = "Date"
    elif data["type"] == "File":
        type_ = "UploadFile"
    elif data["type"] == "Textarea":
        type_ = "Textarea"
    elif data["type"] == "Ueditor":
        type_ = "Ueditor"
    elif data["type"] == "NormalFile":
        type_ = "NormalFile"
    else:
        type_ = "Input"

    model = getattr(app.ext.form, type_)
    model_ = model()
    model_.init_input(data)
    return model_.to_dict()


def make_form(data):
    """
    生成form的json结构
    :param entity:
    :return:
    """
    if isinstance(data.get("form"), str):
        data["form"] = json.loads(data["form"]) if data.get("form") else {}

    type_ = get_form(data).get("type")

    model = getattr(app.ext.serv.form, type_)
    model_ = model()
    model_.init_input(data)
    return model_.to_dict()


def parse_operate_form(name, inputs, display_name, description):
    if "params" in inputs:
        for item in inputs["params"]:
            item["__operate__"] = name

    form_ = OperateFormModel(name)
    form_.init = ""
    form_.object = name
    attrs = inputs.get("params", [])
    if attrs:
        for attr in attrs:
            form_.add_obj(name, display_name, make_operate_form(attr), description)
    else:
        form_.add_obj(name, display_name, description=description)
    return form_


def parse_fun_form(name, inputs, display_name, description):
    form_ = OperateFormModel(name)
    form_.init = ""
    form_.object = name
    attrs = inputs.get("params", [])
    if attrs:
        for attr in attrs:
            form_.add_obj(name, display_name, make_operate_form(attr), description)
    else:
        form_.add_obj(name, display_name, description=description)
    return form_


def parse_form(schema_, view=None, attrs=None, operate="default"):
    form_ = FormModel(schema_.name, schema_.display_name)
    form_.init = ""
    form_.object = schema_.name
    view_dict = {}

    if view:
        view_dict = json.loads(view.content)
    for attr in schema_.attributes:
        if attr["type"] == "Group" or attr["type"] == "Reverse" or \
                attr["type"] == "Dynamic":
            continue

        if attrs is not None:
            if attr["name"] not in attrs:
                continue
        else:
            if view_dict:
                if not view_dict.get(attr["name"]):
                    continue
        attr["__operate__"] = operate
        item = make_form(attr)
        form_.add_obj(''.join(attr.get("tags", [])), item)
    return form_
