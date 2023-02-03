import os
import json
import random
import dominate
import requests
from dominate.tags import *

TABLE_DIR = "./infogo/records.json"

receiver = {
    "sur_name": "Zhang",
    "given_name": "Quandan",
    "degree": "Prof.",
    "address": "12345678900@163.com"
}

def read_table_json(file_path):
    if not os.path.exists(file_path):
        raise ValueError(f'No such file: {file_path}')

    with open(file_path, mode='r', encoding="utf-8") as f:
        table_json = json.load(f)

    return table_json


class Table():
    def __init__(self, table_dir):
        self.table_dir = table_dir
        self.table_json = read_table_json(self.table_dir)
        try:
            self.make_up_table()
        except KeyError as k:
            msg = f"ERROR: The key {str(k).upper()} was not found in table JSON!"
            self.table = div(msg, style="color:red;font-size:12pt;font-family:serif;text-align:center;margin:0 "
                                        "auto;border-style:solid;width:80%")

    def make_up_table(self):
        self.table = table(style="text-align:center;margin:0 auto;border-collapse:collapse;")
        # set table name
        table_name = f"Table: {self.table_json['table_name']}"
        self.table_title = tr(td(table_name,
                                 colspan=len(self.table_json['table_head']),
                                 style="border-style:none;font-style:oblique;padding:4pt"))
        self.table += self.table_title
        self.set_table_body()

    def set_table_body(self):
        self.table_body = tbody()
        # set table head
        self.table_head = tr()
        for e in self.table_json['table_head']:
            self.table_head += th(e, style="border:2pt;border-style:solid none solid none;padding:6pt")
        self.table_body += self.table_head
        # fill table data
        self.fill_table_data()
        self.table += self.table_body

    def fill_table_data(self):
        num = len(self.table_json["table_content"])
        for idx, record in enumerate(self.table_json["table_content"]):
            table_record = tr()
            for e in record:
                if idx != num - 1:
                    table_record += td(e, style="border-style:none;padding:6pt")
                else:
                    table_record += td(e, style="border:2pt;border-style:none none solid none;padding:6pt")
            self.table_body += table_record


class EmailBody():
    def __init__(self, table_dir):
        self.table_dir = table_dir
        self.email_body = div(style="font-family:Georgia,serif;font-size:14pt;width:60%;vertical-align:middle;margin:0 "
                               "auto;background-color:#F6F5F0;color:#555;padding:30pt;")
        self.receiver = None
        self.signature = "anonymous"
        self._table_description = None

        self.init_email_body()
        self.make_up_email_body()

    def init_email_body(self):
        pass

    def make_up_email_body(self):
        self.set_salutation()
        self.set_opener()
        self.set_table()
        self.set_table_description()
        self.set_prompt()
        self.set_daily_quote()
        self.set_ending()

        print(self.email_body)

    def set_salutation(self):
        greetings = ["Dear", "Hi", "Hello", "Hey"]
        if self.receiver == None:
            self._salutation = f"{random.choice(greetings)},"
        else:
            self._salutation = f"{random.choice(greetings)} {self.receiver['degree']} {self.receiver['sur_name']},"
        self.salutation = div(self._salutation, style="text-align:left;")
        self.email_body += self.salutation

    def set_opener(self):
        opens1 = [
            "Hope this email finds you well.",
            "Hope you are well."
        ]
        opens2 = [
            "Here are the oven-fresh results for the experiment that you might concern about.",
            "Here are the freshly-baked results of the experiment that you may be interested in.",
            "Please check out the results of the freshly-baked experiment. You won't want to miss this."
        ]

        self._opener = f"{random.choice(opens1)} {random.choice(opens2)}"
        self.opener = p(self._opener, style="text-align:left;")
        self.email_body += self.opener

    def set_table(self):
        table = Table(self.table_dir)
        self.table = table.table
        self._table = table.table_json
        self.email_body += self.table

    def set_table_description(self):
        if self._table_description == None:
            return
        self.table_description = div(f"DESCR: {self._table_description}",
                                     style="font-family:serif;text-align:left;margin:10pt auto; "
                                           "border-style:double;width:95%;padding:10pt;")
        self.email_body += self.table_description

    def set_prompt(self):
        tips = [
            "If possible, kindly remind the operator to move on to the next experiment "
            "or to shut down the charged cloud server in time.",
            "Please remind the operator to either start the next experiment "
            "or turn off the cloud server promptly.",
        ]
        self._prompt = random.choice(tips)
        self.prompt = p(self._prompt, style="text-align:left;")
        self.email_body += self.prompt

    def set_daily_quote(self):
        try:
            url = "https://apiv3.shanbay.com/weapps/dailyquote/quote/"
            self._daily_quote = requests.get(url).json()['content']
        except:
            self._daily_quote = ""
        finally:
            self.daily_quote = p(self._daily_quote,
                                 style="text-align:left;font-style:oblique;text-decoration:underline;")
            self.email_body += self.daily_quote

    def set_ending(self):
        ends1 = [
            "Yours sincerely,",
            "Yours truly,",
            "Most sincerely,",
            "Sincerely yours,"
        ]
        self.email_body += br()
        self.end1 = p(random.choice(ends1), style="text-align:left;")
        self.email_body += self.end1
        if self.signature == "anonymous":
            self.end2 = p(style="text-align:left;")
        else:
            self.end2 = p(f"{self.signature} & ", style="text-align:left;")
        self.InfoGO = a("InfoGO", href="https://github.com/gongzhimin/InfoGO")
        self.end2.add(self.InfoGO)
        self.email_body += self.end2


if __name__ == "__main__":
    print('DEBUG...')
    email_body = EmailBody(TABLE_DIR)

    doc = dominate.document(title='hello')
    doc += email_body.email_body
    # save as html file
    with open('test.html', 'w') as f:
        f.write(doc.render())



