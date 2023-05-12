from celery import Celery
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from email.mime.application import MIMEApplication
import os
from os.path import basename

load_dotenv()

SENDER_ADDRESS  = os.environ.get('GMAIL_USER') 
SENDER_PASS     = os.environ.get('GMAIL_PASSWORD')

celery = Celery('tasks',
                broker='redis://redis:6379',
                backend='redis://redis:6379')

@celery.task()
def send_async_email(email_data):

    mail_content = email_data['body']

    message = MIMEMultipart()

    message['From'] = SENDER_ADDRESS
    message['To'] = email_data['to']
    message['Subject'] = email_data['subject']

    message.attach(MIMEText(mail_content, 'plain'))

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(SENDER_ADDRESS, SENDER_PASS)
    text = message.as_string()
    session.sendmail(SENDER_ADDRESS, email_data['to'], text)
    session.quit()

    print('Mail Sent')