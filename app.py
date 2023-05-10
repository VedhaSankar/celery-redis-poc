from flask import Flask, request, session, render_template, flash, redirect, url_for
from celery import Celery
import os
from flask_mail import Mail, Message
import requests

app = Flask(__name__)
mail= Mail(app)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


celery = Celery('app', broker='redis://localhost:6379', backend='redis://localhost:6379')
# celery.config.update(app.config)


SENDER_ADDRESS  = os.environ.get('GMAIL_USER') 
SENDER_PASS     = os.environ.get('GMAIL_PASSWORD')
# EMAIL_LIST      = os.environ.get('EMAIL_LIST')


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

        return render_template('index.html', email=session.get('email', ''))
    
    email = request.form['email']
    
    session['email'] = email

    # send the email
    email_data = {
        'subject': 'Hello from Flask',
        'to': email,
        'body': 'This is a test email sent from a background Celery task.'
    }

    if request.form['submit'] == 'Send':
        # send right away
        send_async_email.delay(email_data)

        flash('Sending email to {0}'.format(email))
    
    else:
        # send in one minute
        send_async_email.apply_async(args=[email_data], countdown=60)
        flash('An email will be sent to {0} in one minute'.format(email))

    return redirect(url_for('index'))

@celery.task
def send_async_email(email_data):
    """Background task to send an email with Flask-Mail."""
    msg = Message(email_data['subject'],
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    
    msg.body = email_data['body']
    with app.app_context():
        mail.send(msg)

if __name__=='__main__':

    app.run(debug = True)