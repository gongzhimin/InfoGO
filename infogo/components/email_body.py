import random
import datetime
import dominate
import requests
from dominate.tags import *


table_dict = {
    "date": "2023-1-21",
    "table_title": "Detection Performance of SLEUTH",
    "table_head": ["AUC", "Logloss", "ASR", "BA"],
    "table_content": [
        [0.80, 0.12, 0.99, 0.98],
        [0.81, 0.11, 0.97, 0.98],
        [0.88, 0.12, 0.99, 0.99]
    ],
    "table_description": "In SLEUTH, encoding and detection are independent on the operation. "
                         "There is no constraint to maintain the consistency of mask size, "
                         "we tag the training data with small mask to keep a strong stealthiness "
                         "and use lager mask during detection. "
}

class Table():
    def __init__(self, table_dict):
        self.table_dict = table_dict
        try:
            self.make_up_table()
        except KeyError as k:
            msg = f"ERROR: The key {str(k).upper()} was not found in table DICT!"
            self._table_title = "Some Real-Time Results Might Be Worth Your Attention"
            self.table = div(msg, style="color:red;font-size:12pt;font-family:serif;text-align:center;margin:0 "
                                        "auto;border-style:solid;width:80%")

    def make_up_table(self):
        self.table = table(style="text-align:center;margin:0 auto;border-collapse:collapse;font-size:14pt;")
        # set table name
        self._table_title = self.table_dict['table_title']
        self.table_title = tr(td(f"Table: {self._table_title}",
                                 colspan=len(self.table_dict['table_head']),
                                 style="border-style:none;font-style:oblique;padding:4pt"))
        self.table += self.table_title
        self.set_table_body()

    def set_table_body(self):
        self.table_body = tbody()
        # set table head
        self.table_head = tr()
        for e in self.table_dict['table_head']:
            self.table_head += th(e, style="border:2pt;border-style:solid none solid none;padding:6pt")
        self.table_body += self.table_head
        # fill table data
        self.fill_table_data()
        self.table += self.table_body

    def fill_table_data(self):
        num = len(self.table_dict["table_content"])
        for idx, record in enumerate(self.table_dict["table_content"]):
            table_record = tr()
            for e in record:
                if idx != num - 1:
                    table_record += td(e, style="border-style:none;padding:6pt")
                else:
                    table_record += td(e, style="border:2pt;border-style:none none solid none;padding:6pt")
            self.table_body += table_record


class EmailBody():
    def __init__(self, table_dict, sendee=None, signature="anonymous"):
        self.table_dict = table_dict
        self.email_body = div(style="font-family:Georgia,serif;font-size:14pt;width:80%;vertical-align:middle;margin:0 "
                               "auto;background-color:#F6F5F0;color:#555;padding:30pt;")
        self.sendee = sendee
        self.signature = signature

        self.make_up_email_body()

    def make_up_email_body(self):
        self.set_salutation()
        self.set_opener()
        self.set_table()
        self.set_table_description()
        self.set_prompt()
        self.set_daily_quote()
        self.set_ending()

        self.email_body = str(self.email_body)
        print(self.email_body)

    def set_salutation(self):
        greetings = ["Dear", "Hi", "Hello", "Hey"]
        if self.sendee == None or self.sendee == "":
            self._salutation = f"{random.choice(greetings)},"
        else:
            self._salutation = f"{random.choice(greetings)} {self.sendee},"
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
        table = Table(self.table_dict)
        today = datetime.date.today()
        self.email_title = f"Experiment: {table._table_title} [{today}]".title()
        self.table = table.table
        self._table = table.table_dict
        self.email_body += self.table

    def set_table_description(self):
        if self.table_dict["table_description"] is None or self.table_dict["table_description"] == "":
            self._table_description = ""
            return

        self._table_description = self.table_dict["table_description"]
        self.table_description = div(f"DESCR: {self._table_description}",
                                     style="font-family:serif;text-align:left;margin:10pt auto; "
                                           "border-style:double;width:80%;padding:10pt;")
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
    email_body = EmailBody(table_dict)

    doc = dominate.document(title='hello')
    doc += email_body.email_body
    # save as html file
    with open('test.html', 'w') as f:
        f.write(doc.render())



