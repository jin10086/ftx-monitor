import yagmail

import os

emailUser = os.environ.get("emailUser", "")
emailPassword = os.environ.get("emailPassword", "")

yag = yagmail.SMTP(user=emailUser, password=emailPassword, host="smtp.163.com")


def sendMail(subject, contents, to):
    yag.send(to, subject, contents)


if __name__ == "__main__":
    pass
