import os
import json
import smtplib
import datetime
from email.header import Header
from email.mime.text import MIMEText

from .email_body import EmailBody


def save_table_json(table_dict, save_dir='./logs'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, f"{datetime.date.today()}.json")
    with open(save_path, 'w') as f:
        json.dump(table_dict, f, ensure_ascii=False, indent=2)


class EmailPostman():
    def __init__(self, table_dict, config=None):
        self.table_dict = table_dict
        self.receivers = config["receivers"]
        self.sender = config["sender"]
        self.make_server()

    def make_server(self):
        self.server = smtplib.SMTP_SSL(self.sender["smtp_server"], 465, timeout=3)
        self.server.set_debuglevel(1)
        self.server.login(self.sender["address"], self.sender["authorization_code"])

    def make_up_email(self, receiver, save_dir="./logs"):
        _email = EmailBody(self.table_dict, receiver["name"], self.sender["name"])
        # email = MIMEText(str(_email.email_body), "html", "utf-8")
        email = MIMEText(str(_email.html_email), "html", "utf-8")
        email["From"] = self.sender["address"]
        email["To"] = receiver["address"]
        email["Subject"] = Header(_email.email_title, "utf-8").encode()
        # save the email
        email_name = f"{self.sender['name']}_{receiver['name']}_[{datetime.date.today()}].html"
        email_path = os.path.join(save_dir, email_name)
        with open(email_path, 'w') as f:
            f.write(_email.html_email)
        return email

    def deliver(self):
        for receiver in self.receivers:
            email = self.make_up_email(receiver)
            self.server.sendmail(self.sender["address"], receiver["address"], email.as_string())
        save_table_json(self.table_dict)
