from datetime import datetime
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib  # SMTP:简单邮件传输协议

class MySendEmail:
    def __init__(self, mail_licence, sender, receiver, subject, content, has_attach=False,
                 attach_dir='', attach_name='',has_img=False, image_dir='', image_name=''):
        '''
        # must provide:
            mail_licence, sender, receiver, subject
        # optional:
            content,
            has_attach, attach_dir, attach_name,
            has_img, image_dir, image_name
        '''
        self.mail_licence = mail_licence
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.content = content
        self.hasAttach = has_attach
        self.attach_dir = attach_dir
        self.attach_name = attach_name
        self.hasImg = has_img
        self.image_dir = image_dir
        self.image_name = image_name

    def __call__(self):
        print('发送邮件中...')
        mm = MIMEMultipart('related')
        mm["From"] = self.sender
        receiver_in_str = ''
        for recv in self.receiver:
            receiver_in_str += recv + ','
        mm["To"] = receiver_in_str[:-1]
        mm["Subject"] = Header(self.subject, 'utf-8')
        message_text = MIMEText(self.content, "plain", "utf-8")
        mm.attach(message_text)

        if self.hasAttach:
            attached = MIMEText(open(self.attach_dir, 'rb').read(), 'base64', 'utf-8')
            attached["Content-Disposition"] = f'attachment; filename={self.attach_name}'
            mm.attach(attached)

        if self.hasImg:
            image_data = open(self.image_dir, 'rb')
            image_stream = MIMEImage(image_data.read())
            image_stream['Content-Type'] = 'application/octet-stream'
            image_stream['Content-Disposition'] = f'attachment; filename={self.image_name}'
            image_data.close()
            mm.attach(image_stream)

        try:
            stp = smtplib.SMTP()
            mail_host = "smtp.163.com"
            stp.connect(mail_host, 25)
            # stp.set_debuglevel(1)  # debuglevel(1)可以打印出和SMTP服务器交互的所有信息
            stp.login(self.sender, self.mail_licence)
            stp.sendmail(self.sender, self.receiver, mm.as_string())  # to_receiver should be a list
            print(f'邮件已于 {datetime.now()} 发送成功!')
            stp.quit()
        except smtplib.SMTPException:
            print('Error: 发送邮件失败！')
