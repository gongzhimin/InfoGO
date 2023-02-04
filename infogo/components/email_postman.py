import os
import json
import smtplib
import datetime
import dominate
from email.header import Header
from email.mime.text import MIMEText

from email_body import EmailBody


def load_config(config_dir):
    pass

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


def save_table_json(table_dict, save_dir='./logs'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, f"{datetime.date.today()}.json")
    with open(save_path, 'w') as f:
        json.dump(table_dict, f, ensure_ascii=False, indent=2)


class EmailPostman():
    def __init__(self, table_dict):
        self.table_dict = table_dict
        self.receivers = receivers
        self.sender = sender

        self.make_server()

    def init_config(self, config_dir):
        pass

    def make_server(self):
        self.server = smtplib.SMTP_SSL(self.sender["smtp_server"], 465, timeout=3)
        self.server.set_debuglevel(1)
        # self.server.ehlo()
        # self.server.starttls()
        self.server.login(self.sender["address"], self.sender["authorization_code"])

    def make_up_email(self, receiver):
        _email = EmailBody(self.table_dict, receiver["name"], self.sender["name"])
        email = MIMEText(_email.email_body, "html", "utf-8")
        email["From"] = self.sender["address"]
        email["To"] = receiver["address"]
        email["Subject"] = Header(_email.email_title, "utf-8").encode()

        return email

    def deliver(self):
        for receiver in self.receivers:
            email = self.make_up_email(receiver)
            self.server.sendmail(self.sender["address"], receiver["address"], email.as_string())

        save_table_json(self.table_dict)


if __name__ == "__main__":
    print('DEBUG...')
    postman = EmailPostman(table_dict)
    postman.deliver()