import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

email_user = 'pucsdpune11@gmail.com'
email_password = 'Pune@1234'
email_send = 'gaikwadanil2298@gmail.com'

subject = 'subject'

msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['Subject'] = subject

body = 'Hi there, todays Attendence'
msg.attach(MIMEText(body,'plain'))

filename='attendance.xlsx'
attachment  =open(filename,'rb')

part = MIMEBase('application','octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition',"attachment; filename= "+filename)

msg.attach(part)
text = msg.as_string()
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_user,email_password)

server.sendmail(email_user,email_send,text)
server.quit()

exec(open('format.py').read())

