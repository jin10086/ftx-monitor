import yagmail

emailUser = "gaojincpp@163.com"
emailPassword = "VNNNAZOHADZDMYAG"
yag = yagmail.SMTP(user=emailUser, password=emailPassword, host="smtp.163.com")


def sendMail(subject, contents, to):
    yag.send(to, subject, contents)


if __name__ == "__main__":
    pass
