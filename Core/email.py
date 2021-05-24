import smtplib
from email.mime.text import  MIMEText
import re
import time

def is_email(recv_email):
    return re.match("[a-z0-9A-z_\.]*@[0-9a-zA-Z]*\.com", recv_email)

def send_email(recv_email, message):
    #SMTP服务器
    SMTPSever = "smtp.163.com"
    #发邮件的地址
    sender = "yanzhang_a2@163.com"
    #发送这邮箱的密码
    passwd = "OSUBQWTHOZZLXHII"
    #设置发送的内容, 转化为邮件文本
    msg = MIMEText(message, _subtype="html")
    #主题
    msg["Subject"]= "Shared Pdf Sign Up Code"
    #发送者
    msg["From"] = sender
    #创建SMTP 服务器 连接
    mailServer = smtplib.SMTP(SMTPSever,25)
    #登陆邮箱
    mailServer.login(sender,passwd)
    #发送邮件
    try:
        mailServer.sendmail(sender, [recv_email], msg.as_string())
    except smtplib.SMTPRecipientsRefused as e:
        mailServer.quit()
        return False
    #退出邮箱
    mailServer.quit()
    return True
