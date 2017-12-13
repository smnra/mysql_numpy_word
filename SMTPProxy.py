#coding: utf-8
import os
import smtplibproxy as smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE,formatdate
from email.header import Header



class SendMail:
    def __init__(self,receiver,cc,title,mainText,attachments):                 #receiver参数是收件人, title是邮件标题,mainText是邮件正文,attachments 参数是附件路径列表


        self.sender = 'hppall@163.com'
        self.receiver = receiver
        self.cc = cc
        self.subject = title
        self.smtpserver = 'smtp.163.com'
        self.username = 'hppall'
        self.password = '3615165'
        self.msg = MIMEMultipart()

        # 下面是文字部分，也就是纯文本
        self.puretext = MIMEText(mainText,'plain','utf-8')   #中文需参数‘utf-8'，单字节字符不需要
        self.msg.attach(self.puretext)

        for attachment in attachments :  # 循环添加附件
            self.attPart = MIMEApplication(open(attachment, 'rb').read())
            self.attPart.add_header('Content-Disposition', 'attachment', filename = os.path.basename(attachment))
            self.msg.attach(self.attPart)


        '''
        # 首先是xlsx类型的附件
        self.xlsxpart = MIMEApplication(open(xlsxFileName, 'rb').read())
        self.xlsxpart.add_header('Content-Disposition', 'attachment', filename = xlsxFileName)
        self.msg.attach(self.xlsxpart)

        # jpg类型的附件
        self.jpgpart = MIMEApplication(open(jpgFileName, 'rb').read())
        self.jpgpart.add_header('Content-Disposition', 'attachment', filename=jpgFileName)
        self.msg.attach(self.jpgpart)
        '''


    def senmail(self):
        ##  下面开始真正的发送邮件了
        try:
            self.msg['Subject'] = Header(self.subject, 'utf-8')
            self.msg['From'] = 'SO_Server<hppall@163.com>'
            self.msg['To'] = COMMASPACE.join(self.receiver)  # COMMASPACE==', ' 收件人可以是多个，self.receiver 是一个列表
            self.msg['Cc'] = COMMASPACE.join(self.cc)        #抄送 可以是多个邮件地址，self.cc 是一个列表
            self.msg['Date'] = formatdate(localtime=True) # 发送时间，当不设定时，用outlook收邮件会不显示日期，QQ网页邮箱会显示日期
            # MIMIMEText有三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码，二和三可以省略不写
            client = smtplib.SMTP()
            client.connect('smtp.163.com')
            client.login(self.username, self.password)
            client.sendmail(self.sender, self.receiver + self.cc, self.msg.as_string())
            client.quit()
            print('邮件发送成功！')
        except smtplib.SMTPRecipientsRefused:
            print('Recipient refused')
        except smtplib.SMTPAuthenticationError:
            print('Auth error')
        except smtplib.SMTPSenderRefused:
            print('Sender refused')
        except smtplib.SMTPException as e:
            print(e)



if __name__ == '__main__' :
    '''
    sendmail = SendMail(['hppall@163.com','liuleib@mail.xahuilong.com','smnra@163.com'],'Modul Test','proxy,text,xlsx,jpg',['20170922_LTE_TopN.xlsx'])
    sendmail.senmail()
    '''
    import datetime         #导入 时间日期 模块
    
    start_datetime = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d") + '00'  # 昨天的日期 '2017102500'
    end_datetime = datetime.datetime.today().strftime("%Y%m%d") + '00' # 今天的日期 '2017102600'
    filename = r'E:\工具\资料\宝鸡\研究\Python\python3\TopN\20170922_LTE_TopN.xlsx'
        
    
    mailreceiver = ['hppall@163.com','liuleib@mail.xahuilong.com','smnra@163.com']
    mailcc = ['smnrao@outlook.com']
    mailTitle = '3G_TopN小区'
    mailBody = 'WCDMA ' + start_datetime + ' - ' + end_datetime + 'Top 小区. 自动发送,请勿回复!'
    mailAttachments = [filename]

    sendmail = SendMail(mailreceiver, mailcc, mailTitle, mailBody, mailAttachments)    #邮件发送
    sendmail.senmail()
