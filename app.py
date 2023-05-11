from flask import Flask, request, session, render_template, flash, redirect, url_for
import tasks
import os
from flask_mail import Mail, Message
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from email.mime.application import MIMEApplication
import os
from os.path import basename

app = Flask(__name__)
mail= Mail(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

SENDER_ADDRESS  = os.environ.get('GMAIL_USER') 
SENDER_PASS     = os.environ.get('GMAIL_PASSWORD')


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = SENDER_ADDRESS
app.config['MAIL_PASSWORD'] = SENDER_PASS
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        return render_template('index.html')
    
    email = request.form['email']

    # send the email
    email_data = {
        'subject': 'Hello from Flask',
        'to': email,
        'body': 'This is a test email sent from a background Celery task.'
    }

    print(email)

    if request.form['submit'] == 'Send':
        # send right away
        tasks.send_async_email.delay(email_data)

        flash('Sending email to {0}'.format(email))

    else:
        # send in one minute
        tasks.send_async_email.apply_async(args=[email_data], countdown=60)
        flash('An email will be sent to {0} in one minute'.format(email))

    return redirect(url_for('index'))


if __name__=='__main__':

    app.run(debug=True,host="0.0.0.0",port=8500)
