#coding: utf-8
import requests
import smtplib
s = requests.session()
s.proxies = {'http': '10.22.0.238:3128'}          #设置http代理










from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header






sender = 'hppall@163.com'  
receiver = 'smnra@163.com'  
subject = 'KPI结果'  
smtpserver = 'smtp.163.com'  
username = 'hppall'  
password = '3615165'  
msg = MIMEMultipart()

# 下面是文字部分，也就是纯文本
puretext = MIMEText('Pyton自动发送邮件测试内容.','plain','utf-8')#中文需参数‘utf-8'，单字节字符不需要
msg.attach(puretext)



# 首先是xlsx类型的附件
xlsxpart = MIMEApplication(open('test.xlsx', 'rb').read())
xlsxpart.add_header('Content-Disposition', 'attachment', filename='test.xlsx')
msg.attach(xlsxpart)

# jpg类型的附件
jpgpart = MIMEApplication(open('erab.jpg', 'rb').read())
jpgpart.add_header('Content-Disposition', 'attachment', filename='erab.jpg')
msg.attach(jpgpart)




##  下面开始真正的发送邮件了
try:
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = 'SMnRa<hppall@163.com>'
    msg['To'] = "smnra@163.com"
    client = smtplib.SMTP()
    client.connect('smtp.163.com')
    client.login(username, password)
    client.sendmail(sender, receiver, msg.as_string())
    client.quit()
    print('带有各种附件的邮件发送成功！')
except smtplib.SMTPRecipientsRefused:
    print('Recipient refused')
except smtplib.SMTPAuthenticationError:
    print('Auth error')
except smtplib.SMTPSenderRefused:
    print('Sender refused')
except smtplib.SMTPException as e:
    print(e)




'''
msg['Subject'] = Header(subject, 'utf-8')
msg['From'] = 'SMnRa<hppall@163.com>'
msg['To'] = "smnra@163.com"
smtp = smtplib.SMTP()
smtp.connect('smtp.163.com')
smtp.login(username, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()

'''

