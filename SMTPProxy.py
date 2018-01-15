#coding: utf-8

import os
import smtplibproxy as smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE,formatdate
from email.header import Header
from email.mime.image import MIMEImage


class SendMail:
    def __init__(self,receiver,cc,title,mainText,attachments, images):                 #receiver参数是收件人, title是邮件标题,mainText是邮件正文,attachments 参数是附件路径列表 images 为要在正文中显示的图片
        self.sender = 'hppall@163.com'
        self.receiver = receiver
        self.cc = cc
        self.subject = title
        self.smtpserver = 'smtp.163.com'
        self.username = 'hppall'
        self.password = '3615165'
        self.msg = MIMEMultipart('related')

        def addimg(src, imgid):  # 文件路径、图片id     添加图片到邮件的资源列表中 以在后续的html中访问图片资源
            fp = open(src, 'rb')  # 打开文件
            msgImage = MIMEImage(fp.read())  # 读入 msgImage 中
            fp.close()  # 关闭文件
            msgImage.add_header('Content-ID', imgid)
            return msgImage

        for attachment in attachments :  # 循环添加附件
            self.attPart = MIMEApplication(open(attachment, 'rb').read())
            self.attPart.add_header('Content-Disposition', 'attachment', filename = os.path.basename(attachment))
            self.msg.attach(self.attPart)


        html = ''

        tr = """           <tr bgcolor="#EFEBDE" height="100" style="font-size:13px">
                            <td><img src="cid:image_id"></td>
                          </tr>
            """

        tableTitle= """
                    <table width="600" border="0" cellspacing="0" cellpadding="4">
                        <tr bgcolor="#CECFAD" height="20" style="font-size:14px">
                            <td colspan=2> """ +  mainText  +  """   统计图表:</td></tr>"""

        foo = """
                    <tr bgcolor="#CECFAD" height="20" style="font-size:14px">
                            <td colspan=2 align = "center"> SO Server </td></tr>"""

        for i, image in enumerate(images) :
            image_id = 'image_'+ str(i)
            print(os.path.basename(image).split('.')[0]+'_' + image_id)
            self.msg.attach(addimg(image,image_id)) #根据图片路径读取图片,并添加到邮件资源中,图片ID为文件名,不包括扩展名
            html = html + tr.replace('image_id', image_id)      #生成正文的HTML代码


        msgtext = MIMEText(tableTitle + html + foo + '</table>' , "html", "utf-8")
        self.msg.attach(msgtext)

    def senmail(self):
        ##  下面开始真正的发送邮件了
        try:
            self.msg['Subject'] = Header(self.subject, 'utf-8')
            self.msg['From'] = 'SMnRa<hppall@163.com>'
            self.msg['To'] = COMMASPACE.join(self.receiver)  # COMMASPACE==', ' 收件人可以是多个，self.receiver 是一个列表
            self.msg['Cc'] = COMMASPACE.join(self.cc)        #抄送 可以是多个邮件地址，self.cc 是一个列表
            self.msg['Date'] = formatdate(localtime=True) # 发送时间，当不设定时，用outlook收邮件会不显示日期，QQ网页邮箱会显示日期            # MIMIMEText有三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码，二和三可以省略不写
            client = smtplib.SMTP()
            client.connect('123.125.50.138')    #smtp.163.com IP
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
    import datetime         #导入 时间日期 模块
    start_datetime = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d") + '00'  # 昨天的日期 '2017102500'
    end_datetime = datetime.datetime.today().strftime("%Y%m%d") + '00' # 今天的日期 '2017102600'
    filename = r'F:\SMnRa\smnra\python\3\TopN\erab.jpg'
    mailreceiver = ['hppall@163.com','liuleib@mail.xahuilong.com']
    mailcc = ['jing.2.zhang@huanuo-nsb.com','smnra@163.com']
    mailTitle = '3G_TopN小区'
    mailBody = 'WCDMA ' + start_datetime + ' - ' + end_datetime + 'Top 小区. 自动发送,请勿回复!'
    mailAttachments = [filename]

    sendmail = SendMail(mailreceiver, mailcc, mailTitle, mailBody, mailAttachments)    #邮件发送
    sendmail.senmail()
