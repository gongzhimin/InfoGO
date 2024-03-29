import os
import yaml
import datetime

from .components import EmailPostman

class InfoGO():
    def __init__(self, config_file="./infogo/_config.yaml"):
        self.config_file = config_file
        self.init_app()

    def init_app(self):
        if not os.path.exists(self.config_file):
            raise ValueError(f"No such file: {self.config_file}!")
        with open(self.config_file, mode='r', encoding="utf-8") as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

        self.table_dict = {
            "date": str(datetime.date.today()),
            "table_title": "",
            "table_head": [],
            "table_content": [],
            "table_description": ""
        }

    def fed(self, title, head, content, description="", signature=""):
        self.table_dict["table_title"] = title
        self.table_dict["table_head"] = head
        self.table_dict["table_content"] = content
        self.table_dict["table_description"] = description
        if signature != "":
            self.config["sender"]["name"] = signature

    def deliver(self):
        self.postman = EmailPostman(self.table_dict, self.config)
        self.postman.deliver()
