from flask import render_template
from flask_mail import Message
from . import mail

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, sender = 'Flasky Admin <flasky@example.com>', recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)