import re
import smtplib
from email.mime.text import  MIMEText
from HelloWorld.secret import secret
from HelloWorld.secret import logger as log


def is_email(recv_email):
    return re.match("[a-z0-9A-z_\.]*@[0-9a-zA-Z]*\.com", recv_email)

def send_email(recv_email, message):
    log.debug("[ Send Email ] Begin To Send Email To {}".format(recv_email))
    #设置发送的内容, 转化为邮件文本
    msg = MIMEText(message, _subtype="html")
    msg["Subject"]= "Shared Pdf Sign Up Code"
    msg["From"] = secret.SENDER

    #创建SMTP 服务器连接 并登陆
    log.debug("[ Send Email ] Connecting To Smtp Server And Login")
    mailServer = smtplib.SMTP_SSL(secret.SMTP_SERVER, 465, timeout=10)
    mailServer.login(secret.SENDER,secret.SMTP_PASSWD)
    
    try:
        #发送邮件
        log.debug("[ Send Email ] Succeed To Connect Smtp Server Begin To Send Email")
        mailServer.sendmail(secret.SENDER, [recv_email,secret.SENDER], msg.as_string())
    except smtplib.SMTPRecipientsRefused as e:
        log.error("[ Send Email ] Send Email To {} Failed , Because Of {}".format(recv_email, e))
        mailServer.quit()
        return False
        
    #退出邮箱
    mailServer.quit()
    log.debug("[ Send Email ] Finished Msg To {}".format(recv_email))
    return True
