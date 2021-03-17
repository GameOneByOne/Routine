import smtplib
from email.mime.text import  MIMEText
import time

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
    msg["Subject"]= "A Test Message For Python Api"
    #发送者
    msg["From"] = sender
    #创建SMTP 服务器 连接
    mailServer = smtplib.SMTP(SMTPSever,25)
    #登陆邮箱
    mailServer.login(sender,passwd)
    #发送邮件
    mailServer.sendmail(sender, [recv_email], msg.as_string())
    #退出邮箱
    mailServer.quit()

def send_sign_up_email(recv_email):
    message = """
        <h3>Welcome Friend<h3>
        <p>&nbsp;&nbsp;&nbsp;&nbsp; We are gald about received your sign up request, your verify code is {} <p>
    """.format(str(time.time()).split(".")[-1])
    send_email(recv_email, message)

send_sign_up_email("yan.zhang@vixtel.com")