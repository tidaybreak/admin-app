__author__ = 'Ti'

import re
import os
import filecmp
import tempfile

from app.ext import sup_ctr
from app.services.base import BaseService
from jinja2 import Environment, FileSystemLoader

TAG = re.compile('[^%]*%([^%]+)%[^%]*')


class SettingService(BaseService):
    def __init__(self):
        super(SettingService, self).__init__()

    def fetch_list(self, section="", prefix=""):
        query_dict = {
            "filter": {
                "and": {
                    "section": {
                        "like": "{section}%".format(section=section)
                    },
                    "key": {
                        "like": "{prefix}%".format(prefix=prefix)

                    }
                }
            }
        }
        data = super().fetch_list(query_dict=query_dict, to_dict=True)
        return data

    def reload_supervisor_config(self):
        config = {}
        data = self.fetch_list("system")
        items = data["items"]
        for item in items:
            config[item["key"]] = item["value"]
        config.update(sup_ctr.sup_cfg)

        tmpl_path = config["SUPERVISOR_TEMPLATE_PATH"]
        tmpl_folder = os.path.dirname(tmpl_path)
        tmpl_file = os.path.split(tmpl_path)[1]
        sup_cfg_path = os.path.join(tmpl_folder, "supervisord.conf")
        env = Environment(
            loader=FileSystemLoader(tmpl_folder),
            autoescape=False
        )
        template = env.get_template(tmpl_file)
        content = template.render(**config)
        tmp = tempfile.NamedTemporaryFile()
        tmp.write(content.encode())
        tmp.flush()
        no_diff = filecmp.cmp(sup_cfg_path, tmp.name, shallow=False)
        tmp.close()
        if no_diff:
            return no_diff
        with open(sup_cfg_path, "w") as f:
            f.write(content)
        _, changed, _ = sup_ctr.reloadConfig()[0]
        for name in changed:
            sup_ctr.stopProcessGroup(name)
            sup_ctr.removeProcessGroup(name)
            sup_ctr.addProcessGroup(name)
            sup_ctr.startProcessGroup(name)
        return no_diff


    def update_record(self, records, reload_proc=False):
        for record in records:
            query_dict = record["query_dict"]
            update_dict = record["update_dict"]
            ok, msg = self.update(query_dict, update_dict)
            if not ok:
                return ok, msg

        if reload_proc:
            self.reload_supervisor_config()
        return True, "ok"
