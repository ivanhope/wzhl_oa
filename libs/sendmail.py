#coding:utf-8
import sys,os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# to_addr = sys.argv[1].split(',')
# subject = sys.argv[2]
# body = sys.argv[3]

def send_mail(to_addr,subject,body):
    if to_addr == '/':
        return ''
    to_addr_list = to_addr.split(',')
    from_addr = 'oa@xiaoquan.com'
    password = 'RPvg8DD62i3U8o8F'
    smtp_server = 'smtp.qiye.163.com'

    msg = MIMEText('<html>%s</html>' % body,'html','utf-8')
    msg['Subject'] = Header(subject, 'utf-8').encode()

    smtp = smtplib.SMTP()
    smtp.connect(smtp_server)
    smtp.login(from_addr,password)
    smtp.sendmail(from_addr, to_addr_list, msg.as_string())
    smtp.quit()